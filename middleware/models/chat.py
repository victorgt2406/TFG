"""
Ask Model
"""
from pydantic import BaseModel


class ChatModel(BaseModel):
    "API input json"
    message: str
