import json

from fastapi.testclient import TestClient
from sql_app.main import app

client = TestClient(app)
test_product_id = 0


def test_create_product():
    response = client.post(
        "/products/",
        json={"name": "Foo Bar", "description": "The Foo Brothers Production"},
    )
    assert response.status_code == 200
    json_data = json.loads(response.text)

    assert 'Foo Bar' in json_data['name']
    assert 'The Foo Brothers Production' in json_data['description']

    if json_data:
        global test_product_id
        test_product_id = json_data["id"]


def test_update_existing_product():
    response = client.put(
        "/products/",
        json={"name": "Foo Bar", "description": "The Foo Inc."},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_product_id,
        "name": "Foo Bar",
        "description": "The Foo Inc.",
        "offers": []
    }


def test_create_existing_product():
    response = client.post(
        "/products/",
        json={
            "name": "Foo Bar",
            "description": "Duplicated item",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Product name already registered"}


def test_delete_product():
    response = client.delete(
        f'/products/{test_product_id}'
    )
    assert response.status_code == 200
