"Users ask questions"
import os
import aiohttp
from fastapi import APIRouter
from models import AskModel

router = APIRouter()

@router.post("/")
async def ask(req: AskModel):
    llm_host = os.getenv('LLM_HOST')
    llm_port = os.getenv('LLM_PORT')
    url = f"http://{llm_host}:{llm_port}/ask"
    print(f"Asking to LLM on {url}")
    async with aiohttp.ClientSession() as session:
        # Convert the Pydantic model to a JSON string
        data_json = req.model_dump()
        data_str:str = req.model_dump_json()
        print(data_json)
        try:
            async with session.post(url, data=data_str, headers={"Content-Type": "application/json"}) as response:
                if response.status == 200:
                    response_data = await response.json()  # Get the response JSON
                    return response_data  # Return the response data as JSON
                else:
                    return {"error": f"Upstream server responded with status {response.status}"}
        except aiohttp.ClientError as e:
            return {"error": str(e)}