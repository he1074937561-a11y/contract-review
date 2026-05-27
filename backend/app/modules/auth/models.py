from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(50), nullable=False)
    role = Column(String(20), default="reviewer")  # admin / reviewer
    department = Column(String(100), default="")
    created_at = Column(DateTime, server_default=func.now())
