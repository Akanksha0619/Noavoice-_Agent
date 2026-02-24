from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx 
from app.integrations.google.oauth import oauth
from app.services.auth import create_access_token
from app.models.user import User
from app.config.database import get_db
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/auth", tags=["OAuth Auth"])


@router.get("/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # Step 1: Google OAuth token
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    email = user_info["email"]
    name = user_info.get("name")
    picture = user_info.get("picture")

    # Step 2: Save user (only if not exists)
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            email=email,
            name=name,
            profile_image=picture,
            auth_provider="google"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    
    base_url = str(request.base_url).rstrip("/")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/assistants/")
        assistants = response.json()

  
    return JSONResponse(content=assistants)