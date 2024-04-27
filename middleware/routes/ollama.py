"Ollama route"
from fastapi import APIRouter
from config import OllamaSingleton

ollama_client = OllamaSingleton.get_instance()

router = APIRouter()

@router.post("/")
async def chat(req:dict):
    return await ollama_client.chat(**req)
