from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.modules.auth.schemas import LoginRequest, RegisterRequest, LoginResponse, UserResponse
from app.modules.auth.service import login, register
from app.modules.auth.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def api_login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await login(db, req.username, req.password)
    return LoginResponse(access_token=result["access_token"], user=UserResponse.model_validate(result["user"]))


@router.post("/register", response_model=UserResponse)
async def api_register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = await register(db, req)
    return UserResponse.model_validate(user)


@router.get("/me", response_model=UserResponse)
async def api_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
