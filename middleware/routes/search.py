"Search route"
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import OpenSearchSingleton
from utils import search as search_os, get_fields

os_client = OpenSearchSingleton.get_instance()

router = APIRouter()

class SearchModel(BaseModel):
    query: str
    ignore_fields: Optional[list[str]] = None

@router.post("/{index}")
async def search(index:str, req:SearchModel):
    query = req.query
    ignore_fields = req.ignore_fields
    response = await search_os(os_client, query, index, ignore_fields)
    if response == None:
        raise HTTPException(404, "OPENSEARCH INDEX NOT FOUND")
    return response

@router.get("/fields/{index}")
async def fields(index:str):
    response = await get_fields(os_client, index)
    if response == None:
        raise HTTPException(404, "OPENSEARCH INDEX NOT FOUND")
    return response
