from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.config.database import get_db
from app.schemas.assistant_schema import (
    AssistantCreate,
    AssistantData,
    AssistantResponseWrapper,
)
from app.services.assistant_service import AssistantService
from app.services.auth import get_current_user


router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
    dependencies=[Depends(get_current_user)]
)


# ==============================
# CREATE AGENT (WITH DEFAULT TEMPLATE)
# ==============================
@router.post(
    "/create/",
    response_model=AssistantResponseWrapper,
    status_code=status.HTTP_201_CREATED
)
async def create_agent(
    payload: AssistantCreate,
    db: AsyncSession = Depends(get_db),
):
    assistant = await AssistantService.create_assistant(
        db=db,
        data=payload.model_dump()
    )

    return AssistantResponseWrapper(
        success=True,
        message="Assistant created successfully",
        data={
            "assistant": AssistantData.model_validate(assistant)
        }
    )


# ==============================
# GET ALL AGENTS
# ==============================
@router.get(
    "/get_all",
    response_model=AssistantResponseWrapper
)
async def list_agents(
    db: AsyncSession = Depends(get_db),
):
    assistants = await AssistantService.get_all_assistants(db)

    return AssistantResponseWrapper(
        success=True,
        message="Assistants fetched successfully",
        data={
            "assistants": [
                AssistantData.model_validate(a) for a in assistants
            ]
        }
    )


# ==============================
# GET AGENT BY ID
# ==============================
@router.get(
    "/get/{agent_id}",
    response_model=AssistantResponseWrapper
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

    return AssistantResponseWrapper(
        success=True,
        message="Assistant fetched successfully",
        data={
            "assistant": AssistantData.model_validate(assistant)
        }
    )


# ==============================
# UPDATE AGENT (TEMPLATE AUTO UPDATE)
# ==============================
@router.put(
    "/update/{agent_id}",
    response_model=AssistantResponseWrapper
)
async def update_agent(
    agent_id: UUID,
    payload: AssistantCreate,
    db: AsyncSession = Depends(get_db),
):
    updated = await AssistantService.update_assistant(
        db=db,
        assistant_id=agent_id,
        data=payload.model_dump(exclude_unset=True)
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistant not found"
        )

    return AssistantResponseWrapper(
        success=True,
        message="Assistant updated successfully",
        data={
            "assistant": AssistantData.model_validate(updated)
        }
    )


# ==============================
# DELETE AGENT
# ==============================
@router.delete(
    "/delete/{agent_id}",
    response_model=AssistantResponseWrapper
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

    return AssistantResponseWrapper(
        success=True,
        message="Assistant deleted successfully",
        data={}
    )