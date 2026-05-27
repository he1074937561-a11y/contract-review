from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base


class ContractTemplate(Base):
    __tablename__ = "contract_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), default="")
    description = Column(Text, default="")
    file_path = Column(String(500), default="")
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
