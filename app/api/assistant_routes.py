from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.config.database import get_db
from app.schemas.assistant_schema import (
    AssistantCreate,
    AssistantResponse,
)
from app.services.assistant_service import AssistantService

router = APIRouter(prefix="/agents", tags=["Agents"])


# CREATE Assistant
@router.post(
    "/",
    response_model=AssistantResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_agent(
    payload: AssistantCreate,
    db: AsyncSession = Depends(get_db),
):
    return await AssistantService.create_assistant(
        db=db,
        data=payload.model_dump()
    )


# GET ALL Assistants
@router.get(
    "/",
    response_model=List[AssistantResponse]
)
async def list_agents(
    db: AsyncSession = Depends(get_db),
):
    return await AssistantService.get_all_assistants(db)


# GET Assistant by ID
@router.get(
    "/{agent_id}",
    response_model=AssistantResponse
)
async def get_agent(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    assistant = await AssistantService.get_assistant(db, agent_id)

    if not assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistant not found"
        )

    return assistant


# UPDATE Assistant
@router.put(
    "/{agent_id}",
    response_model=AssistantResponse
)
async def update_agent(
    agent_id: UUID,
    payload: AssistantCreate,
    db: AsyncSession = Depends(get_db),
):
    updated = await AssistantService.update_assistant(
        db=db,
        assistant_id=agent_id,
        data=payload.model_dump()
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistant not found"
        )

    return updated


# DELETE Assistant
@router.delete(
    "/{agent_id}",
    status_code=status.HTTP_200_OK
)
async def delete_agent(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    deleted = await AssistantService.delete_assistant(db, agent_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistant not found"
        )

    return {"message": "Assistant deleted successfully"}
