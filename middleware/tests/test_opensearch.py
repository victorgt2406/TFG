import asyncio
import os
from fastapi.testclient import TestClient
import pytest
from main import app
from config import OpenSearchSingleton

client = TestClient(app)
host = os.getenv("OS_HOST") or "opensearch-node"
port = int(os.getenv("OS_PORT") or "9200")

@pytest.mark.asyncio
async def notest_opensearch_connection():
    await OpenSearchSingleton.test_connection()
    await asyncio.sleep(1)  # Simulating an asynchronous operation
    client_info = await OpenSearchSingleton.get_instance().info()
    print("client info", client_info)
    assert client_info

# Sample async function to be tested
async def async_add(a, b):
    
    return a + b

# Asynchronous test function without arguments
@pytest.mark.asyncio
async def test_async_add():
    result = await async_add(1, 2)
    assert result == 3