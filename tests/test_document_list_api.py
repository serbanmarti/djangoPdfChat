import pytest

from api_v1.models import Document


@pytest.mark.django_db
def test_get_no_data(api_client, user) -> None:
    # Authenticate the user
    api_client.force_authenticate(user=user)

    # Get the documents
    response_create = api_client.get('/api/v1/documents/', format='json')

    # Check the response
    assert response_create.status_code == 200
    assert len(response_create.data) == 0


@pytest.mark.django_db
def test_get_with_data(api_client, user) -> None:
    # Authenticate the user
    api_client.force_authenticate(user=user)

    # Create a document
    Document(name='test.pdf', file='uploads/test.pdf', user_id=user.pk).save()

    # Get the documents
    response_create = api_client.get('/api/v1/documents/', format='json')

    # Check the response
    assert response_create.status_code == 200
    assert len(response_create.data) == 1
