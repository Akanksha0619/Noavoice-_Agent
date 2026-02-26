from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.api.assistant_routes import router as assistant_router
from app.api.prompt_routes import router as assistant_prompt_router
from app.api.knowledge_routes import router as knowledge_router
from app.api.voice_routes import router as configure_router
from app.api.auth_routes import router as auth_router
from app.config.settings import settings
from app.config.database import engine
from app.models.base import Base

app = FastAPI(title="NoaVoice Assistant API")


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="noavoice_session",  
    same_site="none",                   
    https_only=True                     
)

@app.get("/")
async def root():
    return {"message": "NovaVoice Backend Running 🚀"}

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Routers
app.include_router(auth_router)
app.include_router(assistant_router)
app.include_router(assistant_prompt_router)
app.include_router(knowledge_router)
app.include_router(configure_router)