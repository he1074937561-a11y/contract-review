from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    contract_type = Column(String(50), default="")
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, default=0)
    file_type = Column(String(20), nullable=False)  # pdf / docx / img
    status = Column(String(20), default="pending")  # pending / reviewing / completed / failed
    raw_text = Column(Text, default="")
    compliance_score = Column(Integer, nullable=True)
    risk_level = Column(String(20), nullable=True)  # high / medium / low
    conclusion = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    reviewed_at = Column(DateTime, nullable=True)
