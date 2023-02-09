import pytest


@pytest.mark.django_db
def test_ad_list(client, ad):
    expected_response = {
    "num_pages": 1,
    "total": 1,
    "items": [
        {
            "id": 11,
            "name": "test ag name",
            "author_id": 11,
            "price": 1,
            "description": "",
            "is_published": False,
            "category": None,
            "image": None
        }
    ]
    }

    response = client.get(
        '/ad/',
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.content == expected_response
