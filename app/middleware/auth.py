from fastapi import Depends
from app.services.auth import oauth2_scheme, verify_token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return payload  # contains email, sub, etc.