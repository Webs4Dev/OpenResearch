import os

from backend.pdf.parser import extract_pdf_pages
from backend.pdf.chunker import build_chunks_from_pages
from backend.rag.vector_store import store_chunks
from backend.pdf.downloader import download_pdf
from backend.utils.pdf import has_pdf

def ingest_paper(paper):
    if not has_pdf(paper):
        return False
    
    os.makedirs("docs/temp",exist_ok=True)
    filename = (paper.title.replace(" ", "_")[:50])
    pdf_path = (f"docs/temp/{filename}.pdf")

    pdf_path = download_pdf(paper.url,pdf_path)

    pages = extract_pdf_pages(pdf_path)
    
    total_chars = sum(
        len(page["text"])
        for page in pages
    )

    print(f"Pages: {len(pages)}")
    print(f"Chars: {total_chars}")

    chunks = build_chunks_from_pages(pages)

    os.remove(pdf_path)

    store_chunks(chunks,paper.title,paper.source)

    return True