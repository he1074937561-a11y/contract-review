from datetime import datetime
from pydantic import BaseModel


class TemplateResponse(BaseModel):
    id: int
    name: str
    type: str
    description: str
    download_count: int
    created_at: datetime

    class Config:
        from_attributes = True
