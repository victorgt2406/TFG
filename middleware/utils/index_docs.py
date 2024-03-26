import json
from opensearchpy.exceptions import ConnectionError as OpenSearchConnectionError
from utils import get_opensearch_client

def docs_to_bulkop_string(documents: list[dict]):
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
        doc_index = doc.get("_index", "data")
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
    print(bulk_op_lines[0])
    # Convert each element to JSON and join with newline characters
    bulk_op_string = '\n'.join(bulk_op_lines)

    return bulk_op_string


def index_docs(docs: list[dict]) -> None:
    "index docs to Opensearch"
    os_client = get_opensearch_client()
    try:
        os_client.bulk(docs_to_bulkop_string(docs))
    except OpenSearchConnectionError:
        print("Error when connecting to OpenSearch")