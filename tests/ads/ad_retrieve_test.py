import pytest


@pytest.mark.django_db
def test_retrieve_ad(client, ad, test_token):
    expected_response = {
        "id": ad.pk,
        "is_published": False,
        "name": "test ad name",
        "price": 1,
        "description": "",
        "image": None,
        "author": ad.author_id,
        "category": ad.category_id
    }

    response = client.get(
        f'/ad/{ad.pk}/',
        HTTP_AUTHORIZATION='Bearer ' + test_token
    )

    assert response.status_code == 200
    assert response.data == expected_response
