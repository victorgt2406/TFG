"""
Ask Model
"""
from typing import Optional
from pydantic import BaseModel


class ContextModel(BaseModel):
    "Context"
    role: str
    content: str



class AppModel(BaseModel):
    "App"
    model: Optional[str] = "llama3"
    name:str
    description: Optional[str] = ""
    terms: Optional[list[ContextModel]] = None
    conclusions: Optional[list[ContextModel]] = None
    ignore_fields: Optional[list[str]] = []

class AppUpdateModel(BaseModel):
    "Update App"
    orig_name: Optional[str]
    name:str
    description: Optional[str] = ""
    terms: Optional[list[ContextModel]] = None
    conclusions: Optional[list[ContextModel]] = None
