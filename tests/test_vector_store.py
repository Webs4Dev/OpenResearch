from backend.pdf.parser import extract_pdf_pages
from backend.pdf.chunker import build_chunks_from_pages
from backend.rag.vector_store import store_chunks,search_chunks

paper_name ="Ai_Agent_Architectures_Survey"
pages = extract_pdf_pages("docs/Ai_Agent_Architectures_Survey.pdf")
chunks = build_chunks_from_pages(pages)

store_chunks(chunks[:10],paper_name)
results = search_chunks("How does AutoGen work?")

print(results)