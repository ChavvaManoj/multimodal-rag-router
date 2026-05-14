from fastapi import APIRouter, UploadFile, File
import os

from app.utils.pdf_parser import extract_text_from_pdf
from app.utils.chunker import chunk_text
from app.services.retrieval_service import create_vector_store

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    extracted_text = ""
    chunks = []
    indexed_chunks = 0

    # PDF Processing
    if file.filename.lower().endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
        chunks = chunk_text(extracted_text)

        # Create FAISS vector store
        if chunks:
            indexed_chunks = create_vector_store(chunks)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully",
        "total_characters": len(extracted_text),
        "total_chunks": len(chunks),
        "indexed_chunks": indexed_chunks,
        "sample_chunk": chunks[0] if chunks else "No chunks created"
    }