from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import search_similar_chunks
from app.services.llm_service import generate_answer

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    query: str


@router.post("/")
def chat(request: ChatRequest):
    relevant_chunks = search_similar_chunks(request.query)

    final_answer = generate_answer(
        query=request.query,
        context_chunks=relevant_chunks
    )

    return {
        "query": request.query,
        "answer": final_answer,
        "relevant_chunks": relevant_chunks
    }