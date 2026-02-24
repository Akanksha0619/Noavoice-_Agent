from openai import OpenAI
from app.config.settings import settings

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class EmbeddingService:
    """
    Production-safe embedding service for RAG
    Works on Render (no heavy ML models)
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