"Handle create and update applications"

# from main import os_client
from models import AppModel
from config.opensearch import os_client

index_body = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "name": {
                "type": "keyword"
            },
            "terms": {
                "type": "nested",
                "properties": {
                    "role": {
                        "type": "text"
                    },
                    "content": {
                        "type": "text"
                    }
                }
            },
            "conclusions": {
                "type": "nested",
                "properties": {
                    "role": {
                        "type": "text"
                    },
                    "content": {
                        "type": "text"
                    }
                }
            }
        }
    }
}

async def handle_update_app(req:dict, index_name = "apps"):
    app:AppModel= AppModel(**req)
    # Check if index exists:
    apps_exists = await os_client.indices.exists(index_name)
    print(f"{index_name} index exists?: {apps_exists}")
    if not apps_exists:
        await os_client.indices.create(index=index_name, body=index_body)
    settings_body = {
        "doc": app.model_dump(),
        "doc_as_upsert": True
    }
    response = await os_client.update(index=index_name, id=app.name, body=settings_body)
    print(response)