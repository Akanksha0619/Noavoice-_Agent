from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.assistant_repository import AssistantRepository
import select

class AssistantService:

    @staticmethod
    async def create_assistant(db: AsyncSession, data: dict):
        return await AssistantRepository.create(db, data)

    @staticmethod
    async def get_all_assistants(db: AsyncSession):
        return await AssistantRepository.get_all(db)

    @staticmethod
    async def get_assistant(db: AsyncSession, assistant_id: UUID):
        return await AssistantRepository.get_by_id(db, str(assistant_id))

    @staticmethod
    async def update_assistant(db: AsyncSession, assistant_id: UUID, data: dict):
        assistant = await AssistantRepository.get_by_id(db, str(assistant_id))
        if not assistant:
            return None

        return await AssistantRepository.update(db, assistant, data)

    @staticmethod
    async def delete_assistant(db: AsyncSession, assistant_id: UUID):
        return await AssistantRepository.delete(db, str(assistant_id))

    @staticmethod
    async def set_prompt(db: AsyncSession, assistant_id: UUID, data: dict):
        return await AssistantRepository.set_prompt(
            db,
            str(assistant_id),
            data
        )

    @staticmethod
    async def delete_prompt(db: AsyncSession, assistant_id: UUID):
        return await AssistantRepository.delete_prompt(
            db,
            str(assistant_id)
        )


    @staticmethod
    async def set_configure(db, assistant_id: str, data: dict):
        result = await db.execute(
            select(assistant).where(assistant.id == assistant_id)
        )
        assistant = result.scalar_one_or_none()

        if not assistant:
            return None

        assistant.voice_name = data.get("voice_name")
        assistant.elevenlabs_voice_id = data.get("elevenlabs_voice_id")
        assistant.language = data.get("language")
        assistant.timezone = data.get("timezone")
        assistant.detect_caller_number = data.get("detect_caller_number")
        assistant.multilingual_support = data.get("multilingual_support")

        await db.commit()
        await db.refresh(assistant)
        return assistant
