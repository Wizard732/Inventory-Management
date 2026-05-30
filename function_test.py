from fastapi.testclient import TestClient
from pydantic import json

from FastAPI.main import app

client = TestClient(app)


def test_get_category():
    info = client.get("/categories")
    assert info.status_code == 200
    print(info.json())

def test_post_category():
    info = {
        "id": 747,
        "name": 'lele',
        "category_id": 1,
        "quantity": 17,
        "price": 600.0
    }
    infons = client.post("/post_categories",json=info)
    assert infons.status_code == 200
    print(infons.json())

def test_get_product():
    info = client.get("/list_product")
    assert info.status_code == 200
    print(info.json())