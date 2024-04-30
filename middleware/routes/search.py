"Search route"
from fastapi import APIRouter
from pydantic import BaseModel
from config import OpenSearchSingleton
from utils import search as search_os
os_client = OpenSearchSingleton.get_instance()

router = APIRouter()

class SearchModel(BaseModel):
    query: str

@router.post("/")
async def search(req:SearchModel):
    query = req.query
    return await search_os(os_client, query)
