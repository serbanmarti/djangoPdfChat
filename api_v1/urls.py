"""
This module contains the URL configuration for the API v1.
"""

from django.urls import path

from api_v1 import views

urlpatterns = [
    path('documents/', views.DocumentList.as_view()),
    path('documents/<uuid:pk>/', views.DocumentDetail.as_view()),
    path('documents/<uuid:pk>/chat', views.DocumentChat.as_view()),
]
