from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import JSONResponse
from app.integrations.google.oauth import oauth
from app.models.user import User
from app.services.auth import create_access_token
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
    # Step 1: Get token from Google
    token = await oauth.google.authorize_access_token(request)

    # Step 2: Get user info from Google
    user_info = token.get("userinfo")

    email = user_info["email"]
    name = user_info.get("name")
    picture = user_info.get("picture")

    # Step 3: Check if user exists
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    # Step 4: Create user if not exists
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

    # ✅ Step 5: Create JWT token
    access_token = create_access_token(
        data={
            "user_id": str(user.id),
            "email": user.email
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name
        }
    }