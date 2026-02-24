from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config.database import get_db
from app.models.assistant import Assistant
from app.schemas.voice_schema import (
    AssistantConfigureCreate,
    AssistantConfigureResponse,
)

router = APIRouter(prefix="/assistants", tags=["Assistant Configure"])



@router.post("/{assistant_id}/configure", response_model=AssistantConfigureResponse)
async def save_configure(
    assistant_id: str,
    data: AssistantConfigureCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assistant).where(Assistant.id == assistant_id)
    )
    assistant = result.scalar_one_or_none()

    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

 
    assistant.voice_name = data.voice_name
    assistant.elevenlabs_voice_id = data.elevenlabs_voice_id
    assistant.language = data.language
    assistant.timezone = data.timezone
    assistant.detect_caller_number = data.detect_caller_number
    assistant.multilingual_support = data.multilingual_support

    await db.commit()
    await db.refresh(assistant)

    return AssistantConfigureResponse(
        assistant_id=assistant.id,
        voice_name=assistant.voice_name,
        elevenlabs_voice_id=assistant.elevenlabs_voice_id,
        language=assistant.language,
        timezone=assistant.timezone,
        detect_caller_number=assistant.detect_caller_number,
        multilingual_support=assistant.multilingual_support,
    )



@router.get("/{assistant_id}/configure", response_model=AssistantConfigureResponse)
async def get_configure(
    assistant_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assistant).where(Assistant.id == assistant_id)
    )
    assistant = result.scalar_one_or_none()

    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

  
    return AssistantConfigureResponse(
        assistant_id=assistant.id,
        voice_name=assistant.voice_name,
        elevenlabs_voice_id=assistant.elevenlabs_voice_id,
        language=assistant.language,
        timezone=assistant.timezone,
        detect_caller_number=assistant.detect_caller_number,
        multilingual_support=assistant.multilingual_support,
    )



@router.delete("/{assistant_id}/configure")
async def reset_configure(
    assistant_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assistant).where(Assistant.id == assistant_id)
    )
    assistant = result.scalar_one_or_none()

    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

    assistant.voice_name = None
    assistant.elevenlabs_voice_id = None
    assistant.language = "English"
    assistant.timezone = None
    assistant.detect_caller_number = False
    assistant.multilingual_support = False

    await db.commit()

    return {"message": "Configure reset successfully"}
