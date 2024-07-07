import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture(scope='function')
def api_client() -> APIClient:
    """
    Fixture to provide an API client
    :return: APIClient
    """
    yield APIClient()


@pytest.fixture(scope='function')
def user() -> User:
    """
    Fixture to provide a user
    :return: User
    """
    user = User(username='tester', email='tester@test.net', password='pytest')
    user.save()

    return user
