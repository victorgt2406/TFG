from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    def contains_any(string:str, word_list:list[str]) -> bool:
        return any(word in string for word in word_list)

    response = client.post("/api/ask/", json={
        "message": "Just name the planets of the solar system."
    })
    assert response.status_code == 200
    assert contains_any(response.json()["answer"], ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])