from backend.retrievers.manager import retrieve_all
from backend.rag.pdf_ingestor import ingest_paper

papers, _, _ = retrieve_all(
    query="multi agent memory systems",
    max_results=1
)

paper = papers[0]

print(paper.title)
print(paper.url)

result = ingest_paper(paper)
print(result)