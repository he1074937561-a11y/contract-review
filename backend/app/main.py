from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.modules.auth.router import router as auth_router
from app.modules.contracts.router import router as contracts_router
from app.modules.risks.router import router as risks_router
from app.modules.reports.router import router as reports_router
from app.modules.chat.router import router as chat_router
from app.modules.templates.router import router as templates_router
from app.modules.admin.router import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="AI Contract Review", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(contracts_router)
app.include_router(risks_router)
app.include_router(reports_router)
app.include_router(chat_router)
app.include_router(templates_router)
app.include_router(admin_router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
