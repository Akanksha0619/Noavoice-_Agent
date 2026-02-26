from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from jose import jwt
import os

from app.config.database import get_db
from app.integrations.google.oauth import oauth
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

# ================= JWT CONFIG =================
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ================= GOOGLE LOGIN =================
@router.get("/google")
async def google_login(request: Request):
    print("Attempting Google login...")
    redirect_uri = str(request.url_for("google_callback"))
    return await oauth.google.authorize_redirect(request, "http://localhost:3000/auth/callback?token={access_token}")


# ================= GOOGLE CALLBACK =================
@router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    try:
        # 1️⃣ Get token from Google
        token = await oauth.google.authorize_access_token(request)
        if not token:
            raise HTTPException(status_code=400, detail="Failed to get Google token")
        print("Google token obtained:", token)  # Debugging statement
        # 2️⃣ Get user info
        user_info = token.get("userinfo")

        if not user_info:
            resp = await oauth.google.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                token=token
            )
            user_info = resp.json()

        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to fetch user info")

        email = user_info.get("email")
        name = user_info.get("name")

        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by Google")

        # 3️⃣ Check existing user
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        # 4️⃣ Create user if not exists (NO profile image)
        if not user:
            user = User(
                email=email,
                name=name,
                auth_provider="google"
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

        # 5️⃣ Create JWT Token
        access_token = create_access_token(
            data={
                "user_id": str(user.id),
                "email": user.email
            }
        )

        # 6️⃣ Final Response
        return {
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "auth_provider": user.auth_provider
            }
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"OAuth Error: {str(e)}"
        )