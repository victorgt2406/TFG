"Search route"
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import OpenSearchSingleton
from utils import search as search_os

os_client = OpenSearchSingleton.get_instance()

router = APIRouter()

class SearchModel(BaseModel):
    query: str
    index: str

@router.post("/")
async def search(req:SearchModel):
    query = req.query
    index = req.index
    response = await search_os(os_client, query, index)
    if response == None:
        raise HTTPException(404, "OPENSEARCH INDEX NOT FOUND")
    return response
