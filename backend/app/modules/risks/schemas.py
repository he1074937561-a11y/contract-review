from datetime import datetime
from pydantic import BaseModel


class RiskItemResponse(BaseModel):
    id: int
    contract_id: int
    clause_index: float
    clause_text: str
    risk_level: str
    category: str
    description: str
    legal_basis: str
    suggestion: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class UpdateRiskStatusRequest(BaseModel):
    status: str
