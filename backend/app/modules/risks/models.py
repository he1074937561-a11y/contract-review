from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base


class RiskItem(Base):
    __tablename__ = "risk_items"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, nullable=False, index=True)
    clause_index = Column(Integer, default=0)
    clause_text = Column(Text, default="")
    risk_level = Column(String(20), nullable=False)  # high / medium / low
    category = Column(String(50), default="")
    description = Column(Text, default="")
    legal_basis = Column(Text, default="")
    suggestion = Column(Text, default="")
    status = Column(String(20), default="active")  # active / ignored / fixed
    created_at = Column(DateTime, server_default=func.now())
