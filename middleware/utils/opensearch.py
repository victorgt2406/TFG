"""
Search for any match with the text to OpenSearch
"""
from opensearchpy import AsyncOpenSearch


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
