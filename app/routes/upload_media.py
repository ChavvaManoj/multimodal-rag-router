from fastapi import APIRouter, UploadFile, File
import os

from app.utils.media_parcer import transcribe_media
from app.utils.chunker import chunk_text
from app.services.retrieval_service import create_vector_store

router = APIRouter(prefix="/upload-media", tags=["Media Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_media(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Transcribe media
    transcript = transcribe_media(file_path)

    # Chunk transcript
    chunks = chunk_text(transcript)

    indexed_chunks = 0

    if chunks:
        indexed_chunks = create_vector_store(
            chunks=chunks,
            source_name=file.filename
        )

    return {
        "filename": file.filename,
        "message": "Media uploaded and transcribed successfully",
        "transcript_characters": len(transcript),
        "total_chunks": len(chunks),
        "indexed_chunks_from_this_file": indexed_chunks,
        "transcript_preview": transcript[:1000]
    }