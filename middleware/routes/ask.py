"Users ask questions"
import os
import aiohttp
from fastapi import APIRouter
from models import AskModel
from utils import get_async_opensearch_client, search, process_llm_terms

router = APIRouter()

@router.post("/")
async def ask(req: AskModel):
    data_str:str = req.model_dump_json()

    # LLM
    llm_host = os.getenv('LLM_HOST')
    llm_port = os.getenv('LLM_PORT')
    llm_url = f"http://{llm_host}:{llm_port}"
    # OpenSearch
    os_client = get_async_opensearch_client()

    # Get terms
    terms:str = ""
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{llm_url}/get_terms", data=data_str, headers={"Content-Type": "application/json"}) as response:
            if response.status == 200:
                response_data = await response.text()
                terms =  str(response_data)
                print(terms)
                terms =  process_llm_terms(terms)
                print(terms)
            else:
                return {"error": f"Upstream server responded with status {response.status}"}
    
    # Get docs
    docs = await search(os_client, terms)
    return docs