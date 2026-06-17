from backend.rag.vector_store import get_embedding
from backend.rag.clients import paper_collection
from backend.utils.logger import log

def store_papers(papers):

    stored = 0
    for paper in papers:
        try:
            text = f"""
                Title:{paper.title}
                Abstract:{paper.abstract}
                """

            embedding = get_embedding(text)
            paper_id = paper_id = f"""{paper.source}_{paper.title.replace(" ","_")}"""

            paper_collection.add(
                ids=[paper_id],
                documents=[text],
                embeddings=[embedding],
                metadatas=[
                    {
                        "paper_title": paper.title,
                        "source": paper.source,
                        "url": paper.url if paper.url else "",
                        "year": int(paper.published_year) if paper.published_year else 0
                    }
                ]
            )
            stored += 1

        except Exception as e:
            log(f"[Rag Error] {e}")       

    log(f"Stored {stored} papers")