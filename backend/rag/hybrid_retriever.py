from backend.rag.vector_store import search_chunks
from backend.rag.paper_store import search_papers
from backend.utils.logger import log

def retrieve_context_hybrid(query,paper_k=5,chunk_k=10):

    papers = search_papers(
        query=query,
        k=paper_k
        )
    
    papers = [paper for paper in papers if paper.get("has_chunks",False)]
    log(f"{len(papers)} papers have usable chunks")
    
    if len(papers)==0:
        chunks = search_chunks(
            query=query,
            k=chunk_k,
        )
        return chunks

    else:
        paper_titles = [paper["paper_title"] for paper in papers]
        all_chunks = []
        for title in paper_titles:
            chunk = search_chunks(
                query=query,
                k=max(chunk_k/paper_k,3),
                paper_title=title
            )
            all_chunks.extend(chunk)
        all_chunks.sort(key=lambda x: x["relevance_score"],reverse=True)

        return all_chunks[:chunk_k]
