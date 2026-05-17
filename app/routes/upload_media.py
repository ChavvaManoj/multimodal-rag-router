from fastapi import APIRouter, UploadFile, File
import os

from app.utils.media_parser import transcribe_media
from app.utils.chunker import chunk_text
from app.services.retrieval_service import create_vector_store

router = APIRouter(prefix="/upload-media", tags=["Media Upload"])

UPLOAD_DIR = "uploads"
TRANSCRIPT_DIR = "transcripts"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)


@router.post("/")
async def upload_media(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Transcribe media
    transcript = transcribe_media(file_path)

    # Save transcript file
    transcript_filename = file.filename.rsplit(".", 1)[0] + ".txt"
    transcript_path = os.path.join(TRANSCRIPT_DIR, transcript_filename)

    with open(transcript_path, "w", encoding="utf-8") as transcript_file:
        transcript_file.write(transcript)

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
        "message": "Media uploaded, transcribed, and stored successfully",
        "transcript_file": transcript_path,
        "transcript_characters": len(transcript),
        "total_chunks": len(chunks),
        "indexed_chunks_from_this_file": indexed_chunks,
        "transcript_preview": transcript[:1000]
    }