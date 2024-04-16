"Users ask questions"
import json
import os
import aiohttp
from fastapi import APIRouter
from models import ChatModel
from utils import get_async_opensearch_client, search
from utils import ollama_get_terms, ollama_get_conclusion
router = APIRouter()

@router.post("/")
async def chat(req: ChatModel):
    message = req.message
    data_str:str = req.model_dump_json()

    # LLM
    ollama_host = os.getenv('OLLAMA_HOST')
    ollama_port = os.getenv('OLLAMA_PORT')
    ollama_url = f"http://{ollama_host}:{ollama_port}"
    # OpenSearch
    os_client = get_async_opensearch_client()

    # Get terms
    terms = await ollama_get_terms(ollama_url, message)
    # print("Terms", terms)
    terms_str = " ".join(terms)

    # Get docs
    docs = await search(os_client, terms_str)
    # print("Docs", docs)

    # Conclusions
    conclusion = await ollama_get_conclusion(ollama_url, message, terms, docs)

    res = {
        "message": message,
        "terms": terms,
        "docs": docs,
        "conclusion": conclusion
    }
    return res