from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_apps_route():
    response = client.get("/api/apps/")
    print(response)
    assert response.status_code == 200


# def test_create_app():
#     response = client.post("/api/apps/",
#                            json={
#                                "name": "test"
#                            })
#     assert response.status_code == 200
