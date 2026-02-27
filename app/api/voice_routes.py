from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import io

from app.config.database import get_db
from app.repository.assistant_repository import AssistantRepository
from app.schemas.voice_schema import (
    AssistantConfigureUpdate,
    AssistantConfigureResponse,
)
from app.config.settings import settings
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/voices",
    tags=["Voice Configuration"],
    dependencies=[Depends(get_current_user)]
)

# ==============================
# 1️⃣ GET SAVED CONFIG (LOAD UI)
# ==============================
@router.get("/{assistant_id}/configure", response_model=AssistantConfigureResponse)
async def get_voice_config(
    assistant_id: str,
    db: AsyncSession = Depends(get_db),
):
    assistant = await AssistantRepository.get_by_id(db, assistant_id)

    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

    return AssistantConfigureResponse(
        assistant_id=assistant.id,
        agent_role=assistant.agent_role,
        voice_name=assistant.voice_name,
        elevenlabs_voice_id=assistant.elevenlabs_voice_id,
        voice_provider=assistant.voice_provider,
        language=assistant.language,
        timezone=assistant.timezone,
        detect_caller_number=assistant.detect_caller_number,
        multilingual_support=assistant.multilingual_support,
        voice_recording=assistant.voice_recording,
    )


# =====================================
# 2️⃣ ADD + UPDATE VOICE CONFIG (SAVE BUTTON)
# =====================================
@router.put("/{assistant_id}/configure", response_model=AssistantConfigureResponse)
async def add_or_update_voice_config(
    assistant_id: str,
    data: AssistantConfigureUpdate,
    db: AsyncSession = Depends(get_db),
):
    assistant = await AssistantRepository.get_by_id(db, assistant_id)

    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

    update_data = data.dict(exclude_unset=True)

    # Smart update (avoid overwriting with None)
    for key, value in update_data.items():
        if value is not None:
            setattr(assistant, key, value)

    await db.commit()
    await db.refresh(assistant)

    return AssistantConfigureResponse(
        assistant_id=assistant.id,
        agent_role=assistant.agent_role,
        voice_name=assistant.voice_name,
        elevenlabs_voice_id=assistant.elevenlabs_voice_id,
        voice_provider=assistant.voice_provider,
        language=assistant.language,
        timezone=assistant.timezone,
        detect_caller_number=assistant.detect_caller_number,
        multilingual_support=assistant.multilingual_support,
        voice_recording=assistant.voice_recording,
    )


# ==============================
# 3️⃣ GET ELEVENLABS VOICES (DROPDOWN)
# ==============================
@router.get("/elevenlabs")
async def get_elevenlabs_voices():
    if not settings.ELEVENLABS_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="ElevenLabs API key is not configured"
        )

    url = "https://api.elevenlabs.io/v1/voices"

    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch voices: {response.text}"
        )

    data = response.json()

    voices = [
        {
            "label": v["name"],
            "value": v["voice_id"],  # IMPORTANT: This is the real ElevenLabs voice_id
            "category": v.get("category"),
            "preview_url": v.get("preview_url"),
        }
        for v in data.get("voices", [])
    ]

    return {"voices": voices}


# ==============================
# 4️⃣ TEST VOICE (🔊 PLAY BUTTON) - FIXED
# ==============================
@router.get("/test/{assistant_id}")
async def test_voice(
    assistant_id: str,
    text: str = Query(default="Hello, this is a test voice from NovaVoice AI assistant."),
    db: AsyncSession = Depends(get_db),
):
    # Debug (remove later)
    print("API KEY:", settings.ELEVENLABS_API_KEY)

    assistant = await AssistantRepository.get_by_id(db, assistant_id)

    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

    if not assistant.elevenlabs_voice_id:
        raise HTTPException(
            status_code=400,
            detail="ElevenLabs voice not configured"
        )

    api_key = settings.ELEVENLABS_API_KEY
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="ELEVENLABS_API_KEY missing in .env"
        )

    voice_id = assistant.elevenlabs_voice_id

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": str(api_key).strip(),
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code == 401:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Invalid ElevenLabs API Key"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"ElevenLabs Error: {response.text}"
        )

    return StreamingResponse(
        io.BytesIO(response.content),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=voice_test.mp3"}
    )