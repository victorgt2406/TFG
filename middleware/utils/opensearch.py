"""
OpenSearch functions to fetch and store data
"""
import os
from opensearchpy import OpenSearch, AsyncOpenSearch

def get_opensearch_client() -> OpenSearch:
    host = os.getenv("OS_HOST") or "opensearch-node"
    port = int(os.getenv("OS_PORT") or "9200")
    user = "admin"
    password = os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD") or "admin"
    auth = (user, password)

    client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False
    )
    return client


def get_async_opensearch_client() -> AsyncOpenSearch:
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
    return client


async def search(os_client: AsyncOpenSearch, text: str):
    "Search terms to OpenSearch"
    index_name = "data"

    body = {
        "size": 3,
        "query": {
            "query_string": {
                "query": text,
                "default_field": "*"
            }
        }
    }

    response = await os_client.search(body, index=index_name)

    res = list(map(
        lambda doc: {
            "_id": doc["_id"],
            "_score": doc["_score"],
            **doc["_source"]
        },
        response["hits"]["hits"]
    ))
    return res
