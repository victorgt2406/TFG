import asyncio
from fastapi.testclient import TestClient
from main import app, os_client

client = TestClient(app)


def test_opensearch_connection():
    def contains_any(string:str, word_list:list[str]) -> bool:
        return any(word in string for word in word_list)
    assert asyncio.run(os_client.info())["tagline"] == "The OpenSearch Project: https://opensearch.org/"