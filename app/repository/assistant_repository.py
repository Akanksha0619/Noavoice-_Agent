from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.assistant import Assistant


class AssistantRepository:

    @staticmethod
    async def create(db: AsyncSession, data: dict):
        assistant = Assistant(**data)
        db.add(assistant)
        await db.commit()
        await db.refresh(assistant)
        return assistant

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Assistant))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, assistant_id: str):
        result = await db.execute(
            select(Assistant).where(Assistant.id == assistant_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, assistant: Assistant, data: dict):
        for key, value in data.items():
            setattr(assistant, key, value)

        await db.commit()
        await db.refresh(assistant)
        return assistant

    @staticmethod
    async def delete(db: AsyncSession, assistant_id: str):
        result = await db.execute(
            delete(Assistant).where(Assistant.id == assistant_id)
        )
        await db.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_prompt(
        db: AsyncSession,
        assistant_id: str,
        data: dict
    ):
        result = await db.execute(
            select(Assistant).where(Assistant.id == assistant_id)
        )
        assistant = result.scalar_one_or_none()

        if not assistant:
            return None

        assistant.first_message = data.get("first_message")
        assistant.system_prompt = data.get("system_prompt")
        assistant.end_call_message = data.get("end_call_message")

        await db.commit()
        await db.refresh(assistant)

        return assistant

    @staticmethod
    async def delete_prompt(db: AsyncSession, assistant_id: str):
        result = await db.execute(
            select(Assistant).where(Assistant.id == assistant_id)
        )
        assistant = result.scalar_one_or_none()

        if not assistant:
            return None

        assistant.first_message = None
        assistant.system_prompt = None
        assistant.end_call_message = None

        await db.commit()
        await db.refresh(assistant)

        return assistant
