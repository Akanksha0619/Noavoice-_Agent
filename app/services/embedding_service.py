from openai import OpenAI
from app.config.settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class EmbeddingService:
    """
    Lightweight embeddings for RAG (Cloud Safe)
    No torch, no sentence-transformers
    """

    @staticmethod
    def get_embedding(text: str) -> list:
        if not text:
            return []

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding