from openai import OpenAI
from app.config.settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class LLMService:

    @staticmethod
    def generate_answer(query: str, context: str) -> str:
        """
        Generate final answer using retrieved context (TRUE RAG)
        Works for any domain and any file type
        """

        prompt = f"""
You are a helpful AI assistant.
Answer the user's question ONLY from the provided context.
If the answer is not in context, say: "Answer not found in uploaded documents."

Context:
{context}

Question:
{query}

Give a clear, short, and accurate answer.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # fast + cheap + best for RAG
            messages=[
                {"role": "system", "content": "You are a document Q&A assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()