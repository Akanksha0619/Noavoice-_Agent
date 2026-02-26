import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.services.rag_service import RAGService
from app.config.database import get_db
from app.repository.knowledge_repository import KnowledgeRepository
from app.schemas.knowledge_schema import KnowledgeResponse
from app.services.file_parser_service import FileParserService
from app.services.llm_service import LLMService
from app.services.auth import get_current_user  # 🔥 CORRECT IMPORT

router = APIRouter(
    prefix="/knowledge",
    tags=["Global Knowledge Base"],
    dependencies=[Depends(get_current_user)]  # 🔐 FIXED AUTH
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 🌍 UPLOAD FILE (PROTECTED)
@router.post("/upload", response_model=KnowledgeResponse)
async def upload_knowledge_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_ext = file.filename.split(".")[-1].lower()

    if file_ext == "pdf":
        content = FileParserService.parse_pdf(file_path)
    elif file_ext == "docx":
        content = FileParserService.parse_docx(file_path)
    elif file_ext == "txt":
        content = FileParserService.parse_txt(file_path)
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only PDF, DOCX, TXT allowed."
        )

    data = {
        "file_name": file.filename,
        "file_type": file_ext,
        "content": content
    }

    knowledge = await KnowledgeRepository.create(db, data)
    return knowledge


# 📚 GET ALL KNOWLEDGE (PROTECTED)
@router.get("/", response_model=List[KnowledgeResponse])
async def get_all_knowledge(
    db: AsyncSession = Depends(get_db),
):
    return await KnowledgeRepository.get_all(db)


# 🗑 DELETE BY ID (PROTECTED)
@router.delete("/{knowledge_id}")
async def delete_knowledge(
    knowledge_id: str,
    db: AsyncSession = Depends(get_db),
):
    deleted = await KnowledgeRepository.delete_by_id(db, knowledge_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Knowledge not found")

    return {"message": "Knowledge deleted successfully"}


# 🧨 DELETE ALL (HIGHLY SENSITIVE - PROTECTED)
@router.delete("/")
async def delete_all_knowledge(
    db: AsyncSession = Depends(get_db),
):
    await KnowledgeRepository.delete_all(db)
    return {"message": "All global knowledge deleted successfully"}


# 🤖 TRUE GENERIC RAG SEARCH (PROTECTED)
@router.get("/rag/search")
async def rag_search(
    query: str,
    db: AsyncSession = Depends(get_db),
):
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    # 1️⃣ Vector Search
    results = await RAGService.semantic_search(db, query, limit=5)

    if not results:
        return {
            "query": query,
            "answer": "No relevant information found in uploaded documents."
        }

    # 2️⃣ Build Context
    context = "\n\n".join([r["content"] for r in results])

    # 3️⃣ LLM Final Answer (TRUE RAG)
    answer = LLMService.generate_answer(query, context)

    return {
        "query": query,
        "answer": answer
    }