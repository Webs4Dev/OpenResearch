from fastapi import APIRouter

from backend.schemas.rag_response import RAGResponse,RAGRequest
from backend.rag.vector_store import retrieve_context
from backend.agents.rag_qa_agent import answer_research_question
from backend.rag.clients import *

router = APIRouter()

@router.get("/stats")
def get_stats():
    return {
        "total_chunks":chunk_collection.count(),
        "total_papers":paper_collection.count()
    }

@router.post("/ask",response_model=RAGResponse)
def ask_question(request:RAGRequest):

    chunks = retrieve_context(
        query=request.question,
        k=request.top_k
    )

    return answer_research_question(
        question=request.question,
        chunks=chunks
    )