from backend.rag.vector_store import search_chunks
from backend.rag.paper_store import search_papers
from backend.utils.logger import log

def retrieve_context_hybrid(query,paper_k=5,chunk_k=10):

    papers = search_papers(
        query=query,
        k=paper_k
        )
    
    paper_titles = [paper["paper_title"] for paper in papers]

    chunks = search_chunks(
        query=query,
        k=chunk_k,
        paper_titles=paper_titles
    )

    return chunks
