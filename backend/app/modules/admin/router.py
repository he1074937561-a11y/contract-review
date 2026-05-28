from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import hash_password
from app.modules.auth.models import User
from app.modules.contracts.models import Contract
from app.modules.admin.models import SystemConfig, OperationLog
from app.modules.admin.schemas import UserCreate, UserUpdate, ConfigUpdate, ConfigResponse
from app.core.config import settings
from app.core.log import log_operation

router = APIRouter(prefix="/api/admin", tags=["admin"])


# ─── Dashboard Stats ───

@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    total = (await db.execute(select(func.count(Contract.id)))).scalar() or 0
    high = (await db.execute(select(func.count(Contract.id)).where(Contract.risk_level == "high"))).scalar() or 0
    avg = (await db.execute(select(func.avg(Contract.compliance_score)))).scalar() or 0
    user_count = (await db.execute(select(func.count(User.id)))).scalar() or 0

    # Contracts by status
    completed = (await db.execute(select(func.count(Contract.id)).where(Contract.status == "completed"))).scalar() or 0
    failed = (await db.execute(select(func.count(Contract.id)).where(Contract.status == "failed"))).scalar() or 0
    reviewing = (await db.execute(select(func.count(Contract.id)).where(Contract.status == "reviewing"))).scalar() or 0
    pending = (await db.execute(select(func.count(Contract.id)).where(Contract.status == "pending"))).scalar() or 0

    # Recent contracts count (last 7 days)
    from sqlalchemy import DateTime
    recent = (await db.execute(
        select(func.count(Contract.id)).where(Contract.created_at >= datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0))
    )).scalar() or 0

    return {
        "total_contracts": total,
        "high_risk": high,
        "avg_score": round(float(avg), 1),
        "total_users": user_count,
        "recent_contracts": recent,
        "contracts_by_status": {
            "completed": completed,
            "failed": failed,
            "reviewing": reviewing,
            "pending": pending,
        },
    }


# ─── User CRUD ───

@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    return [
        {
            "id": u.id,
            "username": u.username,
            "display_name": u.display_name,
            "role": u.role,
            "department": u.department,
            "is_active": u.is_active,
            "created_at": str(u.created_at) if u.created_at else None,
        }
        for u in result.scalars()
    ]


@router.post("/users")
async def create_user(req: UserCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = (await db.execute(select(User).where(User.username == req.username))).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = User(
        username=req.username,
        password_hash=hash_password(req.password),
        display_name=req.display_name,
        role=req.role,
        department=req.department,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await log_operation(db, current_user, "create", "user", user.id, f"创建用户 {req.username}")
    return {"id": user.id, "username": user.username, "display_name": user.display_name, "role": user.role, "department": user.department}


@router.put("/users/{user_id}")
async def update_user(user_id: int, req: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if req.display_name is not None:
        user.display_name = req.display_name
    if req.role is not None:
        user.role = req.role
    if req.department is not None:
        user.department = req.department
    if req.password:
        user.password_hash = hash_password(req.password)
    await db.commit()
    await log_operation(db, current_user, "update", "user", user_id, f"编辑用户 {user.username}")
    return {"ok": True}


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    await db.delete(user)
    await db.commit()
    await log_operation(db, current_user, "delete", "user", user_id, f"删除用户 {user.username}")
    return {"ok": True}


@router.put("/users/{user_id}/status")
async def toggle_user_status(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能禁用自己")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.is_active = not user.is_active
    await db.commit()
    status_text = "启用" if user.is_active else "禁用"
    await log_operation(db, current_user, "toggle_status", "user", user_id, f"{status_text}用户 {user.username}")
    return {"is_active": user.is_active}


# ─── System Config ───

@router.get("/config")
async def get_config(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(SystemConfig))
    configs = {row.key: row.value for row in result.scalars()}
    api_key = configs.get("llm_api_key", "") or settings.LLM_API_KEY
    return ConfigResponse(
        llm_model=configs.get("llm_model", "") or settings.LLM_MODEL,
        llm_base_url=configs.get("llm_base_url", "") or settings.LLM_BASE_URL,
        llm_api_key_masked=api_key[:8] + "****" if api_key and len(api_key) > 8 else ("****" if api_key else ""),
    )


@router.put("/config")
async def update_config(req: ConfigUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    updates = {}
    if req.llm_api_key is not None:
        await _upsert_config(db, "llm_api_key", req.llm_api_key)
        updates["llm_api_key"] = "updated"
    if req.llm_model is not None:
        await _upsert_config(db, "llm_model", req.llm_model)
        updates["llm_model"] = req.llm_model
    if req.llm_base_url is not None:
        await _upsert_config(db, "llm_base_url", req.llm_base_url)
        updates["llm_base_url"] = req.llm_base_url
    await log_operation(db, current_user, "update_config", "config", detail=f"更新配置: {', '.join(updates.keys())}")
    return {"ok": True, "updated": updates}


async def _upsert_config(db: AsyncSession, key: str, value: str):
    result = await db.execute(select(SystemConfig).where(SystemConfig.key == key))
    config = result.scalar_one_or_none()
    if config:
        config.value = value
    else:
        db.add(SystemConfig(key=key, value=value))
    await db.commit()


# ─── Operation Logs ───

@router.get("/logs")
async def list_logs(
    page: int = 1,
    page_size: int = 50,
    action: str = "",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(OperationLog)
    if action:
        query = query.where(OperationLog.action == action)
    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar() or 0
    query = query.order_by(desc(OperationLog.created_at)).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = [
        {
            "id": log.id,
            "user_id": log.user_id,
            "username": log.username,
            "action": log.action,
            "target_type": log.target_type,
            "target_id": log.target_id,
            "detail": log.detail,
            "created_at": str(log.created_at) if log.created_at else None,
        }
        for log in result.scalars()
    ]
    return {"items": items, "total": total}
