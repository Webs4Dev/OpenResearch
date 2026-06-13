from backend.rag.vector_store import collection,get_embedding
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

            collection.add(
                ids=[paper_id],
                documents=[text],
                embeddings=[embedding],
                metadatas=[
                    {
                        "paper_title": paper.title,
                        "source": paper.source,
                        "url": paper.url,
                        "year": paper.year
                    }
                ]
            )

            stored += 1

        except Exception:
            # duplicate paper already exists
            pass

    log(f"Stored {stored} papers")