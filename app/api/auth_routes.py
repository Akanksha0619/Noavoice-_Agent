from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config.database import get_db
from app.integrations.google.oauth import oauth
from app.models.user import User
from app.services.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# ================= GOOGLE LOGIN =================
@router.get("/google")
async def google_login(request: Request):
    redirect_uri = str(request.url_for("google_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


# ================= GOOGLE CALLBACK =================
@router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    try:
        # 1. Get Google token
        token = await oauth.google.authorize_access_token(request)
        if not token:
            raise HTTPException(status_code=400, detail="Failed to get Google token")

        # 2. Get user info
        user_info = token.get("userinfo")
        if not user_info:
            resp = await oauth.google.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                token=token
            )
            user_info = resp.json()

        email = user_info.get("email")
        name = user_info.get("name")

        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by Google")

        # 3. Check if user exists
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        # 4. Create user if not exists
        if not user:
            user = User(
                email=email,
                name=name,
                auth_provider="google"
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

        # 5. Create JWT Token (VERY IMPORTANT)
        access_token = create_access_token(
            data={
                "user_id": str(user.id),
                "email": user.email
            }
        )

        # 6. Return JWT token
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "name": user.name
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OAuth Error: {str(e)}"
        )