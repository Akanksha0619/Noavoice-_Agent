from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.assistant_routes import router as assistant_router
from app.api.prompt_routes import router as assistant_prompt_router
from app.api.knowledge_routes import router as knowledge_router
from app.api.voice_routes import router as configure_router
from app.api.auth_routes import router as auth_router

from app.config.settings import settings
from app.config.database import engine
from app.models.base import Base

from app.models.assistant import Assistant
from app.models.knowledge import Knowledge
from app.models.user import User

app = FastAPI(title="NoaVoice Assistant API")

# 🔐 Session Middleware (REQUIRED for Google OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="noavoice_session",
    same_site="lax",
    https_only=False
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://noavoice-agent.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "NovaVoice Backend Running 🚀"}


@app.on_event("startup")
async def on_startup():
    print("🔥 Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully!")


# Routers
app.include_router(auth_router)
app.include_router(assistant_router)
app.include_router(assistant_prompt_router)
app.include_router(knowledge_router)
app.include_router(configure_router)