"""
OpenSearch functions to fetch and store data
"""
import asyncio
import os
import json
from fastapi import HTTPException
from opensearchpy import OpenSearch, AsyncOpenSearch
from opensearchpy.exceptions import ConnectionError as OpenSearchConnectionError

def get_opensearch_client() -> OpenSearch:
    "Returns a pre-configured synced OpenSearch client"
    host = os.getenv("OS_HOST") or "opensearch-node"
    port = int(os.getenv("OS_PORT") or "9200")
    user = "admin"
    password = os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD") or "admin"
    auth = (user, password)

    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress=True,  # enables gzip compression for request bodies
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False
    )
    return client

def get_async_opensearch_client() -> AsyncOpenSearch:
    "Returns a pre-configured async OpenSearch client"
    host = os.getenv("OS_HOST") or "opensearch-node"
    port = int(os.getenv("OS_PORT") or "9200")
    user = "admin"
    password = os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD") or "admin"
    auth = (user, password)

    client = AsyncOpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress=True,  # enables gzip compression for request bodies
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False
    )
    return client


async def search(os_client: AsyncOpenSearch, terms: str, index: str):
    "Search the text terms using OpenSearch inside the `index` indicated"
    if not await os_client.indices.exists(index):
        return None
    body = {
        "size": 3,
        "query": {
            "query_string": {
                "query": terms,
                "default_field": "*"
            }
        }
    }

    response = await os_client.search(body, index=index)

    res = list(map(
        lambda doc: {
            "_id": doc["_id"],
            "score": doc["_score"],
            **doc["_source"]
        },
        response["hits"]["hits"]
    ))
    return res


def docs_to_bulkop_string(documents: list[dict], index:str):
    """
    Transforms a list of dictionaries into a bulk operation string for OpenSearch,
    where each document contains '_id' and '_index' keys.

    Parameters:
    documents (list): A list of dictionaries, each representing a document.

    Returns:
    str: A string formatted for the OpenSearch bulk API.
    """
    bulk_op_lines = []

    for doc in documents:
        # Basic metadata
        doc_index = doc.get("_index", index)
        doc_id = doc.get("_id", None)

        # Prepare action metadata
        action_meta = {"update": {"_index": doc_index, "_id": doc_id}}

        # Delete _index and _id keys
        if "_id" in doc:
            del doc["_id"]
        if "_index" in doc:
            del doc["_index"]
        doc_data = {
            "doc": doc,
            "doc_as_upsert": True
        }

        # Add action metadata line and document data line
        bulk_op_lines.append(json.dumps(action_meta))
        bulk_op_lines.append(json.dumps(doc_data))
    # Convert each element to JSON and join with newline characters
    bulk_op_string = '\n'.join(bulk_op_lines)

    return bulk_op_string


async def index_docs(docs: list[dict], os_client:AsyncOpenSearch, index:str) -> None:
    "index docs to Opensearch"
    try:
        await os_client.bulk(docs_to_bulkop_string(docs, index))
    except OpenSearchConnectionError:
        print("Error when connecting to OpenSearch")

async def index_docs_auto(docs: list[dict], os_client: AsyncOpenSearch, index: str):
    def divide_list(arr: list, n: int):
        return [arr[i:i + n] for i in range(0, len(arr), n)]

    div_docs = divide_list(docs, 500)
    len_div_docs = len(div_docs)
    
    for i, div_doc in enumerate(div_docs):
        index_docs(div_doc, os_client, index)
        await asyncio.sleep(2)
        print(f"{i+1}/{len_div_docs} indexed.")
