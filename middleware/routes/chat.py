"Users ask questions"
import json
import os
import aiohttp
from fastapi import APIRouter
from models import ChatModel
from utils import get_async_opensearch_client, search

router = APIRouter()

@router.post("/")
async def chat(req: ChatModel):
    message = req.message
    data_str:str = req.model_dump_json()

    # LLM
    llm_host = os.getenv('LLM_HOST')
    llm_port = os.getenv('LLM_PORT')
    llm_url = f"http://{llm_host}:{llm_port}"
    # OpenSearch
    os_client = get_async_opensearch_client()

    # Get terms
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{llm_url}/get_terms", data=data_str, headers={"Content-Type": "application/json"}) as response:
            if response.status == 200:
                terms = await response.json()
                terms_str = " ".join(terms)
            else:
                return {"error": f"Upstream server responded with status {response.status}"}
    
    # Get docs
    docs = await search(os_client, terms_str)

    # Conclusions
    conclusion_msg = f"""From these options : {json.dumps(docs)}
    Which of them is the best for this situation: {message}"""
    data_str = json.dumps({
        "message": conclusion_msg
    })
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{llm_url}/ask", data=data_str, headers={"Content-Type": "application/json"}) as response:
            if response.status == 200:
                conclusion:str = await response.json()
                conclusion = conclusion.replace("\n"," ").strip()
            else:
                return {"error": f"Upstream server responded with status {response.status}"}

    res = {
        "docs": docs,
        "terms": terms,
        "conclusion": conclusion
    }
    return res