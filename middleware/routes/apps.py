"Create application uses for the LSM"

from pydantic import ValidationError
from models import AppModel
from fastapi import APIRouter, HTTPException
from utils import handle_update_app
from config.opensearch import os_client

router = APIRouter()


@router.post("/")
async def create_app(req: dict):
    try:
        settings: AppModel = AppModel.model_validate(req)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return await handle_update_app(settings)


@router.get("/")
async def get_apps():
    body = {
        "size": 1000,
        "query": {
            "match_all": {}
        }
    }

    response:dict = await os_client.search(body, "apps")
    hits = response.get("hits", [])
    hits = hits.get("hits", [])
    documents = list(map(lambda x: x["_source"], hits))

    return documents


@router.get("/{app}")
async def get_app(app:str):
    body = {
        "size": 1,
        "query": {
            "match": {
                "name": app
            }
        }
    }

    response = await os_client.search(body, "apps")
    document = response['hits']['hits'][0]["_source"]

    return document