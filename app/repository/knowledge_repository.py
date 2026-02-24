from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.knowledge import Knowledge
from app.services.embedding_service import EmbeddingService
from app.services.chunking_service import ChunkingService


class KnowledgeRepository:

    @staticmethod
    async def create(db, data: dict):
        content = data.get("content")
        file_name = data.get("file_name")
        file_type = data.get("file_type")

        # 🔥 STEP 1: Split file into chunks (REAL RAG FIX)
        chunks = ChunkingService.chunk_text(content)

        saved_records = []

        for chunk in chunks:
            # 🔥 STEP 2: Create embedding per chunk
            embedding = EmbeddingService.get_embedding(chunk)

            knowledge = Knowledge(
                file_name=file_name,
                file_type=file_type,
                content=chunk,  # store chunk instead of full document
                embedding=embedding
            )

            db.add(knowledge)
            saved_records.append(knowledge)

        await db.commit()

        # return first record (for API response)
        return saved_records[0] if saved_records else None

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Knowledge))
        return result.scalars().all()

    @staticmethod
    async def delete_by_id(db: AsyncSession, knowledge_id: str):
        result = await db.execute(
            delete(Knowledge).where(Knowledge.id == knowledge_id)
        )
        await db.commit()
        return result.rowcount > 0

    @staticmethod
    async def delete_all(db: AsyncSession):
        result = await db.execute(delete(Knowledge))
        await db.commit()
        return result.rowcount > 0