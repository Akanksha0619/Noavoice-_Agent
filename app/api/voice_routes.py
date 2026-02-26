from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.repository.assistant_repository import AssistantRepository
from app.schemas.voice_schema import (
    AssistantConfigureUpdate,
    AssistantConfigureResponse,
)
from app.services.auth import get_current_user


router = APIRouter(
    prefix="/assistants",
    tags=["Assistant Configure"]
)


# ==============================
# GET CONFIGURE (Can be Public or Protected as needed)
# ==============================
@router.get("/{assistant_id}/configure", response_model=AssistantConfigureResponse)
async def get_assistant_configure(
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


# ==============================
# SAVE / UPDATE CONFIGURE (PROTECTED)
# ==============================
@router.put("/{assistant_id}/configure", response_model=AssistantConfigureResponse)
async def update_assistant_configure(
    assistant_id: str,
    data: AssistantConfigureUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),  # 🔐 AUTH HERE
):
    assistant = await AssistantRepository.get_by_id(db, assistant_id)

    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

    update_data = data.dict(exclude_unset=True)

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
# RESET CONFIGURE (PROTECTED)
# ==============================
@router.delete("/{assistant_id}/configure")
async def reset_assistant_configure(
    assistant_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),  # 🔐 AUTH HERE
):
    assistant = await AssistantRepository.get_by_id(db, assistant_id)

    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

    assistant.agent_role = None
    assistant.voice_name = None
    assistant.elevenlabs_voice_id = None
    assistant.voice_provider = "elevenlabs"
    assistant.language = "English"
    assistant.timezone = None
    assistant.detect_caller_number = False
    assistant.multilingual_support = False
    assistant.voice_recording = False

    await db.commit()

    return {"message": "Assistant configuration reset successfully"}