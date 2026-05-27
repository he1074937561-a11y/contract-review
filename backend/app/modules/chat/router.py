from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.deps import get_current_user
from app.modules.chat.models import ChatMessage
from app.modules.chat.schemas import ChatRequest
from app.modules.contracts.models import Contract
from app.llm.deepseek import DeepSeekClient
from app.llm.prompts import CHAT_SYSTEM_PROMPT

router = APIRouter(prefix="/api/contracts/{contract_id}/chat", tags=["chat"])


@router.get("/messages")
async def get_messages(contract_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.contract_id == contract_id)
        .order_by(ChatMessage.created_at)
    )
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "created_at": m.created_at,
        }
        for m in result.scalars()
    ]


@router.post("")
async def chat(contract_id: int, req: ChatRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contract).where(Contract.id == contract_id))
    contract = result.scalar_one_or_none()
    if not contract:
        return {"error": "contract not found"}

    # Save user message
    user_msg = ChatMessage(contract_id=contract_id, role="user", content=req.message)
    db.add(user_msg)
    await db.commit()

    # Get AI response
    client = DeepSeekClient()
    truncated_text = contract.raw_text[:8000] if contract.raw_text else ""
    response = await client.chat([
        {
            "role": "system",
            "content": f"{CHAT_SYSTEM_PROMPT}\n\n当前合同原文如下：\n\n{truncated_text}",
        },
        {"role": "user", "content": req.message},
    ])

    # Save AI message
    ai_msg = ChatMessage(contract_id=contract_id, role="ai", content=response)
    db.add(ai_msg)
    await db.commit()

    return {"role": "ai", "content": response}
