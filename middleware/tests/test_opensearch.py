import asyncio
from fastapi.testclient import TestClient
from main import app
from config import os_client

client = TestClient(app)

def test_opensearch_connection():
    assert asyncio.run(os_client.info())["tagline"] == "The OpenSearch Project: https://opensearch.org/"