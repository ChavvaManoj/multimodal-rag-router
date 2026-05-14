from fastapi import APIRouter
from pydantic import BaseModel
import time

from app.services.retrieval_service import search_similar_chunks
from app.services.llm_service import generate_answer
from app.utils.metrics import log_query_metrics

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    query: str


@router.post("/")
def chat(request: ChatRequest):
    start_time = time.time()

    # Retrieve relevant chunks
    relevant_chunks = search_similar_chunks(request.query)

    # Generate routed response
    llm_response = generate_answer(
        query=request.query,
        context_chunks=relevant_chunks
    )

    # Response time
    response_time = time.time() - start_time

    # Log metrics
    log_query_metrics(
        query=request.query,
        query_type=llm_response["query_type"],
        model_used=llm_response["model_used"],
        response_time=response_time
    )

    return {
        "query": request.query,
        "query_type": llm_response["query_type"],
        "model_used": llm_response["model_used"],
        "estimated_cost": llm_response["estimated_cost"],
        "response_time_seconds": round(response_time, 2),
        "answer": llm_response["answer"],
        "relevant_chunks": relevant_chunks
    }