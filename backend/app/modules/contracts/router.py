import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.deps import get_current_user
from app.modules.auth.models import User
from app.modules.contracts.models import Contract
from app.modules.contracts.schemas import ContractResponse, ContractListItem, ContractListResponse
from app.modules.contracts.service import save_upload_file, extract_text
from app.modules.risks.service import run_review
from app.core.log import log_operation

router = APIRouter(prefix="/api/contracts", tags=["contracts"])


@router.post("/upload", response_model=ContractResponse)
async def upload_contract(
    file: UploadFile = File(...),
    title: str = Form(""),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    file_path, file_name, file_type = save_upload_file(file, current_user.id)
    raw_text = extract_text(file_path, file_type)
    contract = Contract(
        user_id=current_user.id,
        title=title or file_name,
        file_name=file_name,
        file_path=file_path,
        file_size=os.path.getsize(file_path),
        file_type=file_type,
        status="reviewing" if raw_text else "failed",
        raw_text=raw_text,
    )
    db.add(contract)
    await db.commit()
    await db.refresh(contract)
    if contract.status == "reviewing":
        await run_review(db, contract)
    await db.refresh(contract)
    return ContractResponse.model_validate(contract)


@router.get("", response_model=ContractListResponse)
async def list_contracts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str = "",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Contract).where(Contract.user_id == current_user.id)
    if search:
        query = query.where(Contract.title.ilike(f"%{search}%"))
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar()
    query = query.order_by(Contract.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = [ContractListItem.model_validate(c) for c in result.scalars()]
    return ContractListResponse(items=items, total=total)


@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(contract_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Contract).where(Contract.id == contract_id, Contract.user_id == current_user.id))
    contract = result.scalar_one_or_none()
    if not contract:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Contract not found")
    return ContractResponse.model_validate(contract)


@router.delete("/{contract_id}")
async def delete_contract(contract_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Contract).where(Contract.id == contract_id, Contract.user_id == current_user.id))
    contract = result.scalar_one_or_none()
    if contract:
        title = contract.title
        await db.delete(contract)
        await db.commit()
        await log_operation(db, current_user, "delete", "contract", contract_id, f"删除合同 {title}")
    return {"ok": True}


@router.get("/{contract_id}/file")
async def get_contract_file(contract_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    from fastapi.responses import FileResponse
    import os
    result = await db.execute(select(Contract).where(Contract.id == contract_id))
    contract = result.scalar_one_or_none()
    if not contract:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Contract not found")
    file_path = os.path.abspath(contract.file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    return FileResponse(file_path, filename=contract.file_name)
