"""
This module contains the views for the API endpoints.
"""
import os
import uuid

from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from gpt.gpt import file_chat
from .forms import UploadFileForm
from .models import Document
from .serializers import DocumentSerializer, InputSerializer


def get_document_object(pk: uuid, user_id: int) -> Document:
    """
    Get a document object by its primary key and user id.
    :param pk: primary key of the document
    :param user_id: id of the user who created the document
    :return: found document object
    """
    try:
        return Document.objects.get(pk=pk, user_id=user_id)
    except Document.DoesNotExist as exc:
        raise Http404 from exc


class DocumentList(APIView):
    """
    List all documents or create a new document.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    @extend_schema(
        operation_id='getDocuments',
        responses={200: DocumentSerializer}
    )
    def get(request):
        """
        Get all documents for the authenticated user.
        :param request:
        :return:
        """
        # Get all documents for the authenticated user
        documents = Document.objects.filter(
            user_id=request.user.id
        ).order_by(
            '-created_at'
        )

        # Serialize the documents to be returned
        serializer = DocumentSerializer(documents, many=True)

        return Response(serializer.data)

    @staticmethod
    @extend_schema(
        operation_id='uploadDocument',
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {'type': 'string', 'format': 'binary'}
                }
            },
        },
        responses={
            201: None,
            400: {
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string'}
                }
            }
        }
    )
    def post(request):
        """
        Upload a document.
        :param request:
        :return:
        """
        # Validate the form
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() is False:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        # Check if the file is a PDF (this is not a secure check)
        ext = os.path.splitext(str(request.FILES['file']))[1]
        valid_extensions = ['.pdf']
        if not ext.lower() in valid_extensions:
            return Response(
                {'detail': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST
            )

        # Save the document
        Document(file=request.FILES['file'], user_id=request.user.id, name=request.FILES['file']).save()

        return Response(status=status.HTTP_201_CREATED)


class DocumentDetail(APIView):
    """
    Retrieve or delete a document.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    @extend_schema(
        operation_id='getDocument',
        responses={
            200: DocumentSerializer,
            404: {
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string'}
                }
            }
        }
    )
    def get(request, pk):
        """
        Get a document by its primary key and user id.
        :param request:
        :param pk:
        :return:
        """
        # Get the document by its primary key and user id
        document = get_document_object(pk, request.user.id)

        # Serialize the document to be returned
        serializer = DocumentSerializer(document)

        return Response(serializer.data)

    @staticmethod
    @extend_schema(
        operation_id='deleteDocument',
        responses={
            204: None,
            404: {
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string'}
                }
            }
        }
    )
    def delete(request, pk):
        """
        Delete a document by its primary key and user id.
        :param request:
        :param pk:
        :return:
        """
        # Get the document by its primary key and user id
        document = get_document_object(pk, request.user.id)

        # Delete the file from storage
        document.file.delete()

        # Delete the document from the database
        document.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentChat(APIView):
    """
    Chat with GPT-4o about the content of the document.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    @extend_schema(
        operation_id='documentChat',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'input': {'type': 'string'}
                }
            },
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'response': {'type': 'string'}
                }
            },
            404: {
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string'}
                }
            },
            500: {
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string'}
                }
            }
        }
    )
    def post(request, pk):
        """
        Chat with GPT-4o about the content of the document.
        :param request:
        :param pk:
        :return:
        """
        # Validate the input
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get the user input
        user_input = serializer.validated_data['input']

        # Get the document by its primary key and user id
        document = get_document_object(pk, request.user.id)

        # Chat with GPT-4o about the content of the document
        res = file_chat(str(document.file), user_input)

        if 'error' in res:
            return Response({'detail': 'Error handling AI request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'response': res['response']}, status=status.HTTP_200_OK)
