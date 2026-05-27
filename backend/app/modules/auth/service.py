from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.modules.auth.models import User
from app.modules.auth.schemas import RegisterRequest
from app.core.security import hash_password, verify_password, create_access_token


async def register(db: AsyncSession, req: RegisterRequest) -> User:
    result = await db.execute(select(User).where(User.username == req.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(
        username=req.username,
        password_hash=hash_password(req.password),
        display_name=req.display_name,
        department=req.department,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def login(db: AsyncSession, username: str, password: str) -> dict:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.id})
    return {"access_token": token, "user": user}
