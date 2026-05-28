from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    display_name: str
    role: str = "reviewer"
    department: str = ""


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    password: Optional[str] = None


class ConfigUpdate(BaseModel):
    llm_api_key: Optional[str] = None
    llm_model: Optional[str] = None
    llm_base_url: Optional[str] = None


class ConfigResponse(BaseModel):
    llm_model: str = ""
    llm_base_url: str = ""
    # API key is masked in responses
    llm_api_key_masked: str = ""
