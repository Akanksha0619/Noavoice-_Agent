from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.knowledge import Knowledge


class KnowledgeService:

    @staticmethod
    async def get_knowledge_stats(db: AsyncSession):

        # Total documents
        total_docs = await db.scalar(
            select(func.count()).select_from(Knowledge)
        )

        # Processed = embedding generated
        processed_docs = await db.scalar(
            select(func.count()).where(Knowledge.embedding.is_not(None))
        )

        # Pending = embedding not generated
        pending_docs = await db.scalar(
            select(func.count()).where(Knowledge.embedding.is_(None))
        )

        # Storage (calculate from content length)
        total_bytes = await db.scalar(
            select(func.sum(func.length(Knowledge.content)))
        ) or 0

        total_mb = round(total_bytes / (1024 * 1024), 2)

        return {
            "total_documents": total_docs or 0,
            "processed": processed_docs or 0,
            "pending": pending_docs or 0,
            "storage_mb": total_mb
        }