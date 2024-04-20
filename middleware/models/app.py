"""
Ask Model
"""
from typing import Optional
from pydantic import BaseModel


class ContextModel(BaseModel):
    "Context"
    model: Optional[str] = "llama3"
    role: str
    content: str



class AppModel(BaseModel):
    "App"
    name:str
    terms: Optional[list[ContextModel]] = None
    conclusions: Optional[list[ContextModel]] = None
