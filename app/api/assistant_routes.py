from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.config.database import get_db
from app.schemas.assistant_schema import AssistantCreate, AssistantResponse
from app.services.assistant_service import AssistantService
from app.services.auth import get_current_user  # AUTH IMPORT

router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)


# CREATE Assistant (PROTECTED)
@router.post(
    "/create/",
    response_model=AssistantResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_agent(
    payload: AssistantCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔐 AUTH HERE
):
    return await AssistantService.create_assistant(
        db=db,
        data=payload.model_dump()
    )


# GET ALL (PUBLIC - optional)
@router.get(
    "/get_all",
    response_model=List[AssistantResponse]
)
async def list_agents(
    db: AsyncSession = Depends(get_db),
):
    return await AssistantService.get_all_assistants(db)


# UPDATE (PROTECTED)
@router.put(
    "/update/{agent_id}",
    response_model=AssistantResponse
)
async def update_agent(
    agent_id: UUID,
    payload: AssistantCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔐 AUTH
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


# DELETE (PROTECTED)
@router.delete(
    "/delete/{agent_id}",
    status_code=status.HTTP_200_OK
)
async def delete_agent(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔐 AUTH
):
    deleted = await AssistantService.delete_assistant(db, agent_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistant not found"
        )

    return {"message": "Assistant deleted successfully"}