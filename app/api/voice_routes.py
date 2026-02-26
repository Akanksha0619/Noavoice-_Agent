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
# 2️⃣ ADD + UPDATE VOICE (SAVE BUTTON)
# SAME ROUTE FOR BOTH (IMPORTANT)
# =====================================
@router.put("/{assistant_id}/configure", response_model=AssistantConfigureResponse)
async def add_or_update_voice_config(
    assistant_id: str,
    data: AssistantConfigureUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    This single API will:
    - Add voice (first time)
    - Update voice (change voice later)
    - Save full configure settings (like NoaVoice UI)
    """

    assistant = await AssistantRepository.get_by_id(db, assistant_id)

    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

    update_data = data.dict(exclude_unset=True)

    # Smart update (no null overwrite)
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
    url = "https://api.elevenlabs.io/v1/voices"

    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    data = response.json()

    voices = [
        {
            "label": v["name"],
            "value": v["voice_id"],
            "category": v.get("category"),
            "preview_url": v.get("preview_url"),
        }
        for v in data.get("voices", [])
    ]

    return {"voices": voices}


# ==============================
# 4️⃣ TEST VOICE (🔊 PLAY BUTTON)
# ==============================
@router.api_route("/test", methods=["GET", "POST"])
async def test_voice(
    voice_id: str,
    text: str = "Hello, this is a test voice from NovaVoice AI assistant."
):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    audio_stream = io.BytesIO(response.content)

    return StreamingResponse(
        audio_stream,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=voice_test.mp3"}
    )