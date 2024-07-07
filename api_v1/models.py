"""
This file contains the models for the api_v1 app.
"""

import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Document(models.Model):
    """
    Document model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(max_length=64, null=False, blank=False)
    file = models.FileField(upload_to='uploads/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
