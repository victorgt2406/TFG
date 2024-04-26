import os
from fastapi.testclient import TestClient
import pytest
from main import app
from config import os_client

client = TestClient(app)

@pytest.mark.asyncio
async def test_opensearch_connection():
    host = os.getenv("OS_HOST") or "opensearch-node"
    port = int(os.getenv("OS_PORT") or "9200")
    client_info = await os_client.info()
    print("client info", client_info)
    assert client_info["tagline"] == "The OpenSearch Project: https://opensearch.org/"
    client.close()
    client
    # assert (await os_client.info())["tagline"] == "The OpenSearch Project: https://opensearch.org/"