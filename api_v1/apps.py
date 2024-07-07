"""
This file is used to configure the app name for the api_v1 app.
"""

from django.apps import AppConfig


class ApiV1Config(AppConfig):
    """
    Configuration for the api_v1 app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_v1'
