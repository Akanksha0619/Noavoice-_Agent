from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import JSONResponse
from app.integrations.google.oauth import oauth
from app.models.user import User
from app.services.auth import create_access_token
from app.config.database import get_db
import httpx 

router = APIRouter(prefix="/auth", tags=["OAuth Auth"])


from app.config.settings import settings

@router.get("/google")
async def google_login(request: Request):
    redirect_uri = "http://127.0.0.1:8000/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # Step 1: Exchange code for access token
    token = await oauth.google.authorize_access_token(request)

    # Step 2: Get user info from Google (IMPORTANT FIX)
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token['access_token']}"}
        )
        user_info = resp.json()

    email = user_info.get("email")
    name = user_info.get("name")
    picture = user_info.get("picture")

    if not email:
        raise HTTPException(status_code=400, detail="Email not provided by Google")

    # Step 3: Check user in DB
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

    # Step 5: Create JWT token (as you wanted)
    access_token = create_access_token(
        data={
            "user_id": str(user.id),
            "email": user.email
        }
    )

    # Step 6: Return token instead of crash
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "profile_image": user.profile_image
        }
    }