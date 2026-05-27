from datetime import datetime
from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: int
    contract_id: int
    report_number: str
    report_data: dict
    generated_at: datetime

    class Config:
        from_attributes = True
