import os

from backend.pdf.parser import extract_pdf_pages
from backend.pdf.chunker import build_chunks_from_pages
from backend.rag.vector_store import store_chunks
from backend.pdf.downloader import download_pdf
from backend.utils.pdf import has_pdf
from backend.rag.vector_store import collection
from backend.utils.logger import log

def paper_exists(paper_title):
    results = collection.get(
    where={
        "paper_title":paper_title
    }
    )
    return len(results["ids"]) > 0


def ingest_paper(paper):
    if not has_pdf(paper):
        log(f"No pdf available: {paper.title}")
        return False

    if paper_exists(paper.title):
        log(f"Already stored: {paper.title}")
        return False
    
    os.makedirs("docs/temp",exist_ok=True)
    filename = (paper.title.replace(" ", "_")[:50])
    pdf_path = (f"docs/temp/{filename}.pdf")

    pdf_path = download_pdf(paper.url,pdf_path)

    pages = extract_pdf_pages(pdf_path)
    chunks = build_chunks_from_pages(pages)

    os.remove(pdf_path)

    store_chunks(chunks,paper.title,paper.source)

    return True