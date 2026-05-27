from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.deps import get_current_user
from app.modules.risks.models import RiskItem
from app.modules.risks.schemas import RiskItemResponse, UpdateRiskStatusRequest

router = APIRouter(prefix="/api/contracts/{contract_id}/risks", tags=["risks"])


@router.get("")
async def list_risks(contract_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RiskItem).where(RiskItem.contract_id == contract_id).order_by(RiskItem.clause_index)
    )
    return [RiskItemResponse.model_validate(r) for r in result.scalars()]


@router.put("/{risk_id}/status")
async def update_risk_status(
    contract_id: int,
    risk_id: int,
    data: UpdateRiskStatusRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(RiskItem).where(RiskItem.id == risk_id, RiskItem.contract_id == contract_id)
    )
    item = result.scalar_one_or_none()
    if item:
        item.status = data.status
        await db.commit()
    return {"ok": True}
