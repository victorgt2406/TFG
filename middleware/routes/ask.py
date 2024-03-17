"Users ask questions"
import aiohttp
from fastapi import APIRouter
from models import AskModel
router = APIRouter()

@router.post("/")
async def ask(req: AskModel):
    url = "http://localhost:6060/ask"
    async with aiohttp.ClientSession() as session:
        # Convert the Pydantic model to a JSON string
        json_data = req.model_dump_json()
        try:
            async with session.post(url, data=json_data, headers={"Content-Type": "application/json"}) as response:
                if response.status == 200:
                    response_data = await response.json()  # Get the response JSON
                    return response_data  # Return the response data as JSON
                else:
                    return {"error": f"Upstream server responded with status {response.status}"}
        except aiohttp.ClientError as e:
            return {"error": str(e)}

