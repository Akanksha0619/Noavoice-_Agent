from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.knowledge import Knowledge


class KnowledgeRepository:

    # ✅ CREATE GLOBAL KNOWLEDGE
    @staticmethod
    async def create(db: AsyncSession, data: dict):
        knowledge = Knowledge(**data)
        db.add(knowledge)
        await db.commit()
        await db.refresh(knowledge)
        return knowledge

    # 🌍 GET ALL GLOBAL KNOWLEDGE
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Knowledge))
        return result.scalars().all()

    # 🗑️ DELETE SINGLE DOCUMENT
    @staticmethod
    async def delete_by_id(db: AsyncSession, knowledge_id: str):
        result = await db.execute(
            delete(Knowledge).where(Knowledge.id == knowledge_id)
        )
        await db.commit()
        return result.rowcount > 0

    # 🔥 DELETE ALL KNOWLEDGE (GLOBAL RESET)
    @staticmethod
    async def delete_all(db: AsyncSession):
        result = await db.execute(delete(Knowledge))
        await db.commit()
        return result.rowcount > 0
