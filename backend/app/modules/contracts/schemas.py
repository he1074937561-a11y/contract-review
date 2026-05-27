from datetime import datetime
from pydantic import BaseModel


class ContractResponse(BaseModel):
    id: int
    user_id: int
    title: str
    contract_type: str
    file_name: str
    file_size: int
    file_type: str
    status: str
    raw_text: str = ""
    compliance_score: int | None = None
    risk_level: str | None = None
    conclusion: str = ""
    created_at: datetime
    reviewed_at: datetime | None = None

    class Config:
        from_attributes = True


class ContractListItem(BaseModel):
    id: int
    title: str
    contract_type: str
    file_type: str
    status: str
    compliance_score: int | None = None
    risk_level: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class ContractListResponse(BaseModel):
    items: list[ContractListItem]
    total: int
