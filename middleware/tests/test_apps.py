from fastapi.testclient import TestClient
import pytest

from main import app

client = TestClient(app)


data_test = {
    "name": "test2",
    "terms": [
            {
                "model": "llama3",
                "role": "admin",
                "content": "admin content"
            },
        {
                "role": "user",
                "content": "user content"
            }
    ],
    "conclusions": [
        {
            "role": "admin",
            "content": "admin content"
        },
        {
            "model": "llama3",
            "role": "user",
            "content": "user content"
        }
    ]
}


def test_apps_route():
    response = client.get("/api/apps/")
    print(response)
    assert response.status_code == 200


def test_create_app():
    response = client.post("/api/apps/", content=data_test)
    assert response.status_code == 200

def test_get_app_test():
    response = client.get("/api/apps/test")
    assert response.json()["name"] == "test"
