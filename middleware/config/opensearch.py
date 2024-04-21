"OpenSearch client"
import asyncio
import os
from opensearchpy import AsyncOpenSearch
from opensearchpy.exceptions import ConnectionError as OpenSearchConnectionError

def get_async_opensearch_client() -> AsyncOpenSearch:
    "Get OpenSearch async client"
    host = os.getenv("OS_HOST") or "opensearch-node"
    port = int(os.getenv("OS_PORT") or "9200")
    user = "admin"
    password = os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD") or "admin"
    auth = (user, password)

    client = AsyncOpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False
    )

    # Check OpenSearch connection
    # async def check_os_connection(client):
    #     "Check connection with OpenSearch"
    #     try:
    #         response = (await client.info())["tagline"]
    #         if(response != "The OpenSearch Project: https://opensearch.org/"):
    #             print("ERROR: Can not connect to OpenSearch.")
    #             raise OpenSearchConnectionError()
    #     except OpenSearchConnectionError as e:
    #         print(f"ERROR: Can not connect to OpenSearch.\n{e}")
    #         raise OpenSearchConnectionError() from e
    #     print("Connected to OpenSearch")
    # # asyncio.run(check_os_connection(client))
    # await check_os_connection(client)

    # body = {
    #     "size": 1000,
    #     "query": {
    #         "match_all": {}
    #     }
    # }

    # response:dict = await client.search(body, "apps")
    # print(response)

    return client

os_client = get_async_opensearch_client()