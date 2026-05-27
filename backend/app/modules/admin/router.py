from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.modules.contracts.models import Contract
from app.modules.auth.models import User

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    total = (await db.execute(select(func.count(Contract.id)))).scalar()
    high = (
        await db.execute(
            select(func.count(Contract.id)).where(Contract.risk_level == "high")
        )
    ).scalar()
    avg = (await db.execute(select(func.avg(Contract.compliance_score)))).scalar() or 0
    return {
        "total_contracts": total or 0,
        "high_risk": high or 0,
        "avg_score": round(float(avg), 1),
    }


@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return [
        {
            "id": u.id,
            "username": u.username,
            "display_name": u.display_name,
            "role": u.role,
            "department": u.department,
        }
        for u in result.scalars()
    ]
