from backend.rag.clients import paper_collection,chunk_collection
from backend.utils.hash import generate_paper_id


paper = paper_collection.get(
    where={
        "paper_title":"T-RAG: Lessons from the LLM Trenches"
    }
)

chunk = chunk_collection.get(
    where={
        "paper_title":"T-RAG: Lessons from the LLM Trenches"
    },
    limit=1
) 

print (paper["metadatas"])
print("\n")
print(chunk['metadatas'])
