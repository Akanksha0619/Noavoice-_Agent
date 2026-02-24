from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.services.embedding_service import EmbeddingService


class RAGService:

    @staticmethod
    async def semantic_search(db: AsyncSession, query: str, limit: int = 3):
        # 1️⃣ Generate query embedding
        query_embedding = EmbeddingService.get_embedding(query)

        if not query_embedding:
            return []

        # 2️⃣ Convert list → pgvector string (VERY IMPORTANT)
        vector_str = "[" + ",".join(map(str, query_embedding)) + "]"

        stmt = text("""
            SELECT id, content, file_name
            FROM knowledge
            WHERE embedding IS NOT NULL
            ORDER BY embedding <-> CAST(:embedding AS vector)
            LIMIT :limit
        """)

        result = await db.execute(
            stmt,
            {"embedding": vector_str, "limit": limit}
        )

        rows = result.fetchall()

        return [
            {
                "id": row.id,
                "content": row.content,
                "file_name": row.file_name
            }
            for row in rows
        ]