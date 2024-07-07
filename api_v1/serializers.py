"""
Serializers for the API.
"""

from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Document model.
    """

    class Meta:
        model = Document
        fields = ('id', 'name', 'file', 'created_at')


class InputSerializer(serializers.Serializer):
    """
    Serializer for the input field.
    """
    input = serializers.CharField(min_length=1, max_length=128)

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        instance.input = validated_data.get('input', instance.input)
        return instance
