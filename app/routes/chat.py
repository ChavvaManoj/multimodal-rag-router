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

    llm_response = generate_answer(
        query=request.query,
        context_chunks=relevant_chunks
    )

    return {
        "query": request.query,
        "query_type": llm_response["query_type"],
        "model_used": llm_response["model_used"],
        "answer": llm_response["answer"],
        "relevant_chunks": relevant_chunks
    }