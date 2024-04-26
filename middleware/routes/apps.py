"Create application uses for the LSM"

from pydantic import ValidationError
from models import AppModel, AppUpdateModel
from fastapi import APIRouter, HTTPException
from utils import handle_update_app
from config.opensearch import os_client

router = APIRouter()
OS_INDEX = "apps"
OS_INDEX_ID = "name"


@router.post("/")
async def merge_app(req: dict):
    try:
        app: AppModel = AppModel.model_validate(req)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return await handle_update_app(app)


@router.delete("/")
async def delete_app(app_name: str):
    try:
        await os_client.delete(OS_INDEX,app_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return



@router.patch("/")
async def update_app(req: dict):
    try:
        req_app: AppUpdateModel = AppUpdateModel.model_validate(req)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    
    if "orig_name" in req_app:
        orig_name = req_app.orig_name
        name = req_app.name
        app:AppModel = await get_app(orig_name)
        app.name = name
        merge_app(app)
    else:
        await get_app(req_app.name) # Check if it exists, so it can be updated
        merge_app(req_app)

    return await handle_update_app(req_app)


@router.get("/")
async def get_apps():
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


@router.get("/{app}")
async def get_app(app_name: str) -> AppModel:
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
