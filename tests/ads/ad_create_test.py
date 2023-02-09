import pytest


@pytest.mark.django_db
def test_create_ad(client, test_token):
    expected_response = {
        "id": 1,
        "is_published": False,
        "name": "1234567890",
        "price": 1,
        "description": "",
        "image": None,
        "author": None,
        "category": None
    }

    data = {
        "is_published": False,
        "name": "1234567890",
        "price": 1
    }

    response = client.post(
        '/ad/create/',
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION='Bearer ' + test_token
        )

    assert response.status_code == 201
    assert response.data == expected_response


