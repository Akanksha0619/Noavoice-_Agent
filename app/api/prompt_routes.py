from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.config.database import get_db
from app.services.assistant_service import AssistantService
from app.services.auth import get_current_user
from app.schemas.assistant_schema import AssistantResponseWrapper, AssistantData
from app.schemas.assistant_prompt_schema import AssistantPromptCreate  


router = APIRouter(
    prefix="/prompts",
    tags=["Assistant Prompts"],
    dependencies=[Depends(get_current_user)]
)


# ==============================
# UPDATE PROMPT (FIRST MESSAGE + SYSTEM PROMPT + END CALL)
# ==============================
@router.put(
    "/update/{agent_id}",
    response_model=AssistantResponseWrapper
)
async def update_prompt(
    agent_id: UUID,
    payload: AssistantPromptCreate,
    db: AsyncSession = Depends(get_db),
):
    assistant = await AssistantService.update_assistant(
        db=db,
        assistant_id=agent_id,
        data=payload.model_dump(exclude_unset=True)
    )

    if not assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistant not found"
        )

    return AssistantResponseWrapper(
        success=True,
        message="Assistant prompt updated successfully",
        data={
            "assistant": AssistantData.model_validate(assistant)
        }
    )


# ==============================
# GET PROMPT BY AGENT ID
# ==============================
@router.get(
    "/get/{agent_id}",
    response_model=AssistantResponseWrapper
)
async def get_prompt(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    assistant = await AssistantService.get_assistant(db, agent_id)

    if not assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistant not found"
        )

    return AssistantResponseWrapper(
        success=True,
        message="Assistant prompt fetched successfully",
        data={
            "assistant_id": str(assistant.id),
            "first_message": assistant.first_message,
            "system_prompt": assistant.system_prompt,
            "end_call_message": assistant.end_call_message,
        }
    )