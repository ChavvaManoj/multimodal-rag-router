from fastapi import FastAPI
from app.routes import chat, upload, upload_media
app = FastAPI(title="Multi-Modal RAG Router")

app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(upload_media.router)

@app.get("/")
def home():
    return {"message": "RAG Router API is running"}