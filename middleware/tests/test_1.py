from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert response.json() == {"message": "Lista de usuarios para versión específica en v1_0"}