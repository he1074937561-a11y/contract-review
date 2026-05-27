from sqlalchemy import Column, Integer, String, Text, DateTime, func, JSON
from app.core.database import Base


class ReviewReport(Base):
    __tablename__ = "review_reports"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, nullable=False, index=True, unique=True)
    report_data = Column(JSON, default={})
    report_number = Column(String(50), default="")
    generated_at = Column(DateTime, server_default=func.now())
