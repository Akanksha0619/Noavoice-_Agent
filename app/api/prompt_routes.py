from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.config.database import get_db
from app.schemas.assistant_prompt_schema import (
    AssistantPromptCreate,
    AssistantPromptResponse,
)
from app.services.assistant_service import AssistantService

router = APIRouter(prefix="/agents", tags=["Assistant Prompt"])


# CREATE / UPDATE Prompt
@router.post(
    "/{agent_id}/prompt",
    response_model=AssistantPromptResponse,
    status_code=status.HTTP_200_OK,
)
async def create_or_update_prompt(
    agent_id: UUID,
    data: AssistantPromptCreate,
    db: AsyncSession = Depends(get_db),
):
    assistant = await AssistantService.set_prompt(
        db=db,
        assistant_id=agent_id,
        data=data.model_dump(),
    )

    if not assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )

    return AssistantPromptResponse(
        assistant_id=assistant.id,
        first_message=assistant.first_message,
        system_prompt=assistant.system_prompt,
        end_call_message=assistant.end_call_message,
    )


# GET Prompt
@router.get(
    "/{agent_id}/prompt",
    response_model=AssistantPromptResponse,
)
async def get_prompt(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    assistant = await AssistantService.get_assistant(db, agent_id)

    if not assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )

    return AssistantPromptResponse(
        assistant_id=assistant.id,
        first_message=assistant.first_message,
        system_prompt=assistant.system_prompt,
        end_call_message=assistant.end_call_message,
    )


# DELETE Prompt (Reset Prompt)
@router.delete(
    "/{agent_id}/prompt",
    status_code=status.HTTP_200_OK,
)
async def delete_prompt(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    assistant = await AssistantService.delete_prompt(
        db=db,
        assistant_id=agent_id,
    )

    if not assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )

    return {"message": "Prompt reset successfully"}
