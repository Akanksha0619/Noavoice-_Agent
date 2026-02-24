from sentence_transformers import SentenceTransformer
from typing import List


class EmbeddingService:
    """
    Convert text into vector embeddings for RAG
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")

    @staticmethod
    def get_embedding(text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        if not text:
            return None
        embedding = EmbeddingService.model.encode(text)
        return embedding.tolist()
    