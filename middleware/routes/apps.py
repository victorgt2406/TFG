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
    "Creates the app or updates it for convenience"
    return await handle_update_app(app)


@router.delete("/{app_name}")
async def delete_app(app_name: str):
    "Deletes the app chosen"
    if not await os_client.indices.exists(OS_INDEX):
        raise HTTPException(400, f"OpenSearch index \"{OS_INDEX}\" is not created.")

    if await os_client.exists(OS_INDEX, app_name) and await os_client.indices.exists(app_name):
        await os_client.delete(OS_INDEX, app_name)
        print(f"{app_name} metadata was deleted.")
        await os_client.indices.delete(app_name)
        print(f"{app_name} index was deleted.")
        return True
    else:
        raise HTTPException(404, f"The app \"{app_name}\" does not exists.")


@router.patch("/")
async def update_app(app: AppUpdateModel):
    "Method to update the application with the complexity of renaming the name which is used as the id"

    # Verificamos que podamos realizar la operación
    if app.name == app.orig_name:
        raise HTTPException(400, "VALUE ERROR. The name_orig and name are equal.")
    if not await os_client.indices.exists(OS_INDEX):
        raise HTTPException(400, f"OpenSearch index \"{OS_INDEX}\" is not created.")
    
    # En caso de querer renombrar la aplicación
    if app.orig_name:
        orig_name = app.orig_name
        name = app.name

        # Verificamos que orig_app exista
        if not await os_client.exists(OS_INDEX, orig_name):
            raise HTTPException(404, f"The app {orig_name} is not founded at \"{OS_INDEX}\" index.")
        
        # Reindex los datos al nuevo índice
        await os_client.reindex({
            "source": {
                "index": orig_name
            },
            "dest": {
                "index": name
            }
        })
        print(f"{orig_name} index data was indexed to {name}.")

        # borramos el indice original
        await delete_app(orig_name)

    # En caso solo de actualizar la app sin renombrar
    elif not await os_client.exists(OS_INDEX, app.name):
        raise HTTPException(404, f"The app {app.name} is not founded at \"{OS_INDEX}\" index.")
    app_dict:dict = app.model_dump()
    del app_dict["orig_name"]
    return await handle_update_app(app_dict)


@router.get("/")
async def get_apps():
    "Returns all the metadata every application"
    
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
    "Returns the metadata of an application"

    if not await os_client.indices.exists(OS_INDEX):
        raise HTTPException(400, f"OpenSearch index \"{OS_INDEX}\" is not created.")

    if not await os_client.exists(OS_INDEX, app_name):
        raise HTTPException(404, f"The app {app_name} is not founded at \"{OS_INDEX}\" index.")

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
