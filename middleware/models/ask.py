"""
Ask Model
"""
from pydantic import BaseModel


class AskModel(BaseModel):
    "API input json"
    message: str
