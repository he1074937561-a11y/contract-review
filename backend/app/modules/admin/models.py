from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base


class SystemConfig(Base):
    __tablename__ = "system_config"

    key = Column(String(100), primary_key=True)
    value = Column(Text, default="")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class OperationLog(Base):
    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    username = Column(String(50), default="")
    action = Column(String(50), nullable=False, index=True)  # upload / delete / create / update / toggle_status / update_config
    target_type = Column(String(50), default="")  # contract / risk / user / config
    target_id = Column(Integer, nullable=True)
    detail = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now(), index=True)
