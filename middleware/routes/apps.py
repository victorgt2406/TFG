"Create application uses for the LSM"
from fastapi import APIRouter, HTTPException
from models import AppModel, AppUpdateModel
from utils import handle_update_app
from config.opensearch import os_client

router = APIRouter()
OS_INDEX = "apps"
OS_INDEX_ID = "name"


@router.post("/")
async def merge_app(app: AppModel):
    return await handle_update_app(app)


@router.delete("/{app_name}")
async def delete_app(app_name: str):
    if not await os_client.indices.exists(OS_INDEX):
        raise HTTPException(400, f"OpenSearch index \"{OS_INDEX}\" is not created.")
    
    if await os_client.exists(OS_INDEX, app_name) and await os_client.indices.exists(app_name):
        await os_client.delete(OS_INDEX, app_name)
        await os_client.indices.delete(app_name)
        return True
    else:
        raise HTTPException(404, f"The app \"{app_name}\" does not exists.")


@router.patch("/")
async def update_app(app: AppUpdateModel):
    if not await os_client.indices.exists(OS_INDEX):
        raise HTTPException(400, f"OpenSearch index \"{OS_INDEX}\" is not created.")
    if "orig_name" in app:
        orig_name = app.orig_name
        name = app.name
        app:AppModel = await get_app(orig_name)
        app.name = name
        merge_app(app)
    else:
        await get_app(app.name) # Check if it exists, so it can be updated
        merge_app(app)

    return await handle_update_app(app)


@router.get("/")
async def get_apps():
    if not await os_client.indices.exists(OS_INDEX):
        raise HTTPException(400, f"OpenSearch index \"{OS_INDEX}\" is not created.")
    body = {
        "size": 1000,
        "query": {
            "match_all": {}
        }
    }

    response: dict = await os_client.search(body, "apps")
    hits = response.get("hits", [])
    hits = hits.get("hits", [])
    documents = list(map(lambda x: x["_source"], hits))

    return documents


@router.get("/{app_name}")
async def get_app(app_name: str) -> AppModel:
    if not await os_client.indices.exists(OS_INDEX):
        raise HTTPException(400, f"OpenSearch index \"{OS_INDEX}\" is not created.")
    body = {
        "size": 1,
        "query": {
            "match": {
                "name": app_name
            }
        }
    }

    response = await os_client.search(body, OS_INDEX)
    if len(response['hits']['hits']) > 0:
        document = response['hits']['hits'][0]["_source"]
        return document
    else:
        raise HTTPException(status_code=404)
