from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.modules.templates.models import ContractTemplate

router = APIRouter(prefix="/api/templates", tags=["templates"])


@router.get("")
async def list_templates(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ContractTemplate).order_by(ContractTemplate.created_at.desc())
    )
    return [
        {
            "id": t.id,
            "name": t.name,
            "type": t.type,
            "description": t.description,
            "download_count": t.download_count,
        }
        for t in result.scalars()
    ]


@router.post("")
async def create_template(data: dict, db: AsyncSession = Depends(get_db)):
    t = ContractTemplate(
        name=data["name"],
        type=data.get("type", ""),
        description=data.get("description", ""),
    )
    db.add(t)
    await db.commit()
    await db.refresh(t)
    return {"id": t.id, "name": t.name}


@router.delete("/{template_id}")
async def delete_template(template_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ContractTemplate).where(ContractTemplate.id == template_id)
    )
    t = result.scalar_one_or_none()
    if t:
        await db.delete(t)
        await db.commit()
    return {"ok": True}
