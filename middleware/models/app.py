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
    description: Optional[str]
    terms: Optional[list[ContextModel]] = None
    conclusions: Optional[list[ContextModel]] = None

class AppUpdateModel(BaseModel):
    "Update App"
    orig_name: Optional[str]
    name:str
    description: Optional[str]
    terms: Optional[list[ContextModel]] = None
    conclusions: Optional[list[ContextModel]] = None
