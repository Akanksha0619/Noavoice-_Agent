import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.config.database import get_db
from app.repository.knowledge_repository import KnowledgeRepository
from app.schemas.knowledge_schema import KnowledgeResponse
from app.services.file_parser_service import FileParserService

router = APIRouter(prefix="/knowledge", tags=["Global Knowledge Base"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 🌍 UPLOAD FILE (GLOBAL KB - PDF/DOCX/TXT)
@router.post("/upload", response_model=KnowledgeResponse)
async def upload_knowledge_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file locally
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_ext = file.filename.split(".")[-1].lower()

    # Parse file content
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


@router.get("/", response_model=List[KnowledgeResponse])
async def get_all_knowledge(
    db: AsyncSession = Depends(get_db),
):
    return await KnowledgeRepository.get_all(db)


# 🗑️ DELETE SINGLE KNOWLEDGE FILE
@router.delete("/{knowledge_id}")
async def delete_knowledge(
    knowledge_id: str,
    db: AsyncSession = Depends(get_db),
):
    deleted = await KnowledgeRepository.delete_by_id(db, knowledge_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Knowledge not found")

    return {"message": "Knowledge deleted successfully"}


# DELETE ALL GLOBAL KNOWLEDGE (RESET KB)
@router.delete("/")
async def delete_all_knowledge(
    db: AsyncSession = Depends(get_db),
):
    await KnowledgeRepository.delete_all(db)
    return {"message": "All global knowledge deleted successfully"}
