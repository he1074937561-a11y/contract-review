from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, nullable=False, index=True)
    role = Column(String(10), nullable=False)  # user / ai
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
