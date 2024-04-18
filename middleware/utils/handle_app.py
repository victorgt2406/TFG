"Handle create and update applications"

# from main import os_client
from models import AppModel
from config.opensearch import os_client

index_name = "apps"

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

async def handle_update_app(settings:dict):
    settings:AppModel= AppModel(**settings)
    # Check if index exists:
    apps_exists = await os_client.indices.exists(index_name)
    print(f"app index exists?: {apps_exists}")
    if not apps_exists:
        await os_client.indices.create(index=index_name, body=index_body)
    settings_body = {
        "doc": settings.model_dump(),
        "doc_as_upsert": True
    }
    response = await os_client.update(index=index_name, id=settings.name, body=settings_body)
    print(response)