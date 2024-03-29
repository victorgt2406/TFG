"""
Models needed for the API
"""
from pydantic import BaseModel


class ContextModel(BaseModel):
    "API input json"
    context: str
