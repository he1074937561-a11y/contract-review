from app.modules.admin.models import OperationLog


async def log_operation(db, user, action: str, target_type: str = "", target_id: int | None = None, detail: str = ""):
    entry = OperationLog(
        user_id=user.id,
        username=user.username,
        action=action,
        target_type=target_type,
        target_id=target_id,
        detail=detail,
    )
    db.add(entry)
    await db.commit()
