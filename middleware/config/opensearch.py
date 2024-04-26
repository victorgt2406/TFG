import asyncio
import os
from opensearchpy import AsyncOpenSearch

class AsyncOpenSearchSingleton:
    _client = None

    @classmethod
    def get_instance(cls):
        if cls._client is None:
            cls._client = cls._create_client()
        return cls._client

    @staticmethod
    def _create_client():
        host = os.getenv("OS_HOST") or "opensearch-node"
        port = int(os.getenv("OS_PORT") or "9200")
        user = "admin"
        password = os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD") or "admin"
        auth = (user, password)

        return AsyncOpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_compress=True,
            http_auth=auth,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )
    
    @classmethod
    async def test_connection(cls):
        client_info = await cls._client.info()
        if client_info["tagline"] != "The OpenSearch Project: https://opensearch.org/":
            print("❌ Not connected to OpenSearch")
        else:
            print("✅ Connection to OpenSearch successful")

os_client = AsyncOpenSearchSingleton.get_instance()
asyncio.run(AsyncOpenSearchSingleton.test_connection())