from fastapi import APIRouter

from backend.schemas.rag_response import RAGResponse,RAGRequest
from backend.rag.hybrid_retriever import retrieve_context_hybrid
from backend.agents.rag_qa_agent import answer_research_question
from backend.rag.clients import *

router = APIRouter()

@router.get("/stats")
def get_stats():
    papers = paper_collection.count()
    chunks = chunk_collection.count()
    avg_chunks = papers/chunks if papers else 0 

    return {
        "total_papers":papers,
        "total_chunks":chunks,
        "avg_chunks_per_paper":round(avg_chunks,2)
    }

@router.post("/ask",response_model=RAGResponse)
def ask_question(request:RAGRequest):

    chunks = retrieve_context_hybrid(
        query=request.question,
        paper_k=request.paper_k,
        chunk_k=request.chunk_k
    )

    return answer_research_question(
        question=request.question,
        chunks=chunks
    )