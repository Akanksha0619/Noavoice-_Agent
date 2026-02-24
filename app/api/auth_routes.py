from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import JSONResponse
from app.integrations.google.oauth import oauth
from app.models.user import User
from app.config.database import get_db

router = APIRouter(prefix="/auth", tags=["OAuth Auth"])


@router.get("/google")
async def google_login(request: Request):
    redirect_uri = "http://127.0.0.1:8000/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # Get token from Google
    token = await oauth.google.authorize_access_token(request)

    # Stable user info fetch (no id_token issue)
    resp = await oauth.google.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        token=token
    )
    user_info = resp.json()

    email = user_info["email"]
    name = user_info.get("name")
    picture = user_info.get("picture")

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

    return JSONResponse(
        content={
            "message": "Login successful",
            "email": user.email,
            "name": user.name
        }
    )