from backend.rag.vector_store import get_embedding
from backend.utils.hash import generate_paper_id
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

            paper_id = generate_paper_id(paper.title)

            paper_collection.add(
                ids=[paper_id],
                documents=[text],
                embeddings=[embedding],
                metadatas=[
                    {
                        "paper_title": paper.title,
                        "source": paper.source,
                        "url": paper.url if paper.url else "",
                        "year": int(paper.published_year) if paper.published_year else 0,
                        "has_chunks":False
                    }
                ]
            )
            stored += 1

        except Exception as e:
            log(f"[Rag Error] {e}")       

    log(f"Stored {stored} papers")


def search_papers(query:str,k:int=5):

    query_embeddings = get_embedding(query)

    results = paper_collection.query(
        query_embeddings=[query_embeddings],
        n_results=k
    )
    log(f"Retrieved {len(results["metadatas"][0])} papers")

    for metadata in results["metadatas"][0]:
        print(metadata)

    papers = []

    for metadata,distance in zip(results["metadatas"][0],results["distances"][0]):
        papers.append(
            {
                "paper_title":metadata["paper_title"],
                "source":metadata["source"],
                "url":metadata["url"],
                "year":metadata["year"],
                "has_chunks":metadata["has_chunks"],
                "distance":distance
            }
        )
    
    return papers

def get_paper_metadata(paper_title:str):
    results = paper_collection.get(
        where={
            "paper_title":paper_title
        }
    )

    if not results["metadatas"]:
        return None
    else:
        return results["metadatas"][0]

    
