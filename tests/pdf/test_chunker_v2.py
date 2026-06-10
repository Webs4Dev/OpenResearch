from backend.pdf.chunker import build_chunks_from_pages
from backend.pdf.parser import extract_pdf_pages

pages = extract_pdf_pages("docs/Ai_Agent_Architectures_Survey.pdf")
chunks = build_chunks_from_pages(pages)

for chunk in chunks[0:11]:
    print()
    print(chunk.chunk_id)
    print(chunk.page_no)
    print(chunk.length)