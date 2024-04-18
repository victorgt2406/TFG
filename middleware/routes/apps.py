"Create application uses for the LSM"

from models import AppModel
from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def create_app(req: AppModel):
    name = req.name


