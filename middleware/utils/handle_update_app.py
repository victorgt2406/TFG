"Handle create and update applications"

import sys
import os

# Add the parent directory to sys.path
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from main import os_client
from models import AppModel

# Define the index name
index_name = "apps"

# Index configuration
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
    


if __name__ == "__main__":
    import asyncio
    settings_model:AppModel = {
        "name": "drugs"
    }
    asyncio.run(handle_update_app(settings_model))