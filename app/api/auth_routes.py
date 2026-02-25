# from fastapi import APIRouter, Request, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from fastapi.responses import JSONResponse
# from app.integrations.google.oauth import oauth
# from app.models.user import User
# from app.services.auth import create_access_token
# from app.config.database import get_db
# import httpx 

# router = APIRouter(prefix="/auth", tags=["OAuth Auth"])


# from app.config.settings import settings

# @router.get("/google")
# async def google_login(request: Request):
#     redirect_uri = "http://127.0.0.1:8000/auth/google/callback"
#     return await oauth.google.authorize_redirect(request, redirect_uri)


# @router.get("/google/callback")
# async def google_callback(
#     request: Request,
#     db: AsyncSession = Depends(get_db)
# ):
#     # Step 1: Exchange code for access token
#     token = await oauth.google.authorize_access_token(request)

#     # Step 2: Get user info from Google (IMPORTANT FIX)
#     async with httpx.AsyncClient() as client:
#         resp = await client.get(
#             "https://www.googleapis.com/oauth2/v2/userinfo",
#             headers={"Authorization": f"Bearer {token['access_token']}"}
#         )
#         user_info = resp.json()

#     email = user_info.get("email")
#     name = user_info.get("name")
#     picture = user_info.get("picture")

#     if not email:
#         raise HTTPException(status_code=400, detail="Email not provided by Google")

#     # Step 3: Check user in DB
#     result = await db.execute(
#         select(User).where(User.email == email)
#     )
#     user = result.scalar_one_or_none()

#     # Step 4: Create user if not exists
#     if not user:
#         user = User(
#             email=email,
#             name=name,
#             profile_image=picture,
#             auth_provider="google"
#         )
#         db.add(user)
#         await db.commit()
#         await db.refresh(user)

#     # Step 5: Create JWT token (as you wanted)
#     access_token = create_access_token(
#         data={
#             "user_id": str(user.id),
#             "email": user.email
#         }
#     )

#     # Step 6: Return token instead of crash
#     return {
#         "message": "Login successful",
#         "access_token": access_token,
#         "token_type": "bearer",
#         "user": {
#             "id": str(user.id),
#             "email": user.email,
#             "name": user.name,
#             "profile_image": user.profile_image
#         }
#     }
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config.database import get_db
from app.integrations.google.oauth import oauth
from app.services.auth import create_access_token
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["OAuth"])


# 🔐 GOOGLE LOGIN (ONLY ONE ROUTE - NO DUPLICATE)
@router.get("/google")
async def google_login(request: Request):
    # 🔥 Dynamic redirect (works for localhost + render both)
    redirect_uri = str(request.url_for("google_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


# 🔁 GOOGLE CALLBACK (MUST HAVE NAME)
@router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    try:
        # 1️⃣ Exchange code for token
        token = await oauth.google.authorize_access_token(request)

        if not token:
            raise HTTPException(status_code=400, detail="Failed to get token from Google")

        # 2️⃣ Get user info safely
        user_info = token.get("userinfo")

        # Fallback if userinfo not auto included
        if not user_info:
            resp = await oauth.google.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                token=token
            )
            user_info = resp.json()

        if not user_info or "email" not in user_info:
            raise HTTPException(status_code=400, detail="Failed to fetch user info")

        email = user_info["email"]
        name = user_info.get("name")
        picture = user_info.get("picture")

        # 3️⃣ Check existing user
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        # 4️⃣ Create new user if not exists
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

        # 5️⃣ Generate JWT token
        access_token = create_access_token(
            data={
                "user_id": str(user.id),
                "email": user.email
            }
        )

        # 6️⃣ Final response (Frontend can store token)
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

    except Exception as e:
        import traceback
        traceback.print_exc()  # 🔥 Important for Render logs
        raise HTTPException(status_code=500, detail=f"OAuth Error: {str(e)}")