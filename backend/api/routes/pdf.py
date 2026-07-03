from fastapi import APIRouter,UploadFile,File,Form
from pathlib import Path
from fastapi import HTTPException
from fastapi.responses import FileResponse
import fitz

from backend.pdf.parser import extract_pdf_pages
from backend.pdf.chunker import build_chunks_from_pages
from backend.rag.vector_store import store_chunks,search_chunks
from backend.agents.project_relevance_agent import sort_relevant_chunks
from backend.agents.pdf_qa_agent import answer_question
from backend.schemas.pdf import *
from backend.utils.hash import generate_paper_id
from backend.utils.logger import log

router = APIRouter()

@router.post("/ingest",response_model=PDFIngestResponse)
async def ingest_pdf(file:UploadFile=File(...)):
    paper_id = generate_paper_id(file.filename)
    temp_path=(f"docs/pdfs/{paper_id}.pdf")
    contents=(await file.read())

    log(f"PDF uploaded: {file.filename}")
    with open(temp_path,'wb') as f:
        f.write(contents)

    pages=extract_pdf_pages(temp_path)
    total_pages=len(fitz.open(temp_path))
    log(f"Extracted {total_pages} pages from {file.filename}")

    chunks = build_chunks_from_pages(pages)
    log(f"Created {len(chunks)} chunks")

    store_chunks(
        paper_title=file.filename,
        chunks=chunks
    )

    return PDFIngestResponse(
        filename=file.filename,
        paper_id=paper_id,
        pages=total_pages,
        chunks_stored=len(chunks)
    )

@router.post("/analyze",response_model=PDFAnalysisResponse)
async def analyze_pdf(file:UploadFile=File(...),project_description:str=Form(...)):
    paper_id = generate_paper_id(file.filename)
    temp_path=(f"docs/pdfs/{paper_id}.pdf")
    contents=(await file.read())

    log(f"PDF uploaded: {file.filename}")
    with open(temp_path,"wb") as f:
        f.write(contents)

    pages=extract_pdf_pages(temp_path)
    total_pages=len(fitz.open(temp_path))
    log(f"Extracted {total_pages} pages from {file.filename}")

    chunks = build_chunks_from_pages(pages)
    log(f"Created {len(chunks)} chunks")

    relevant_chunks = sort_relevant_chunks(
        chunks=chunks,
        project_description=project_description,
        top_k=5
    )

    chunk_map = {chunk.chunk_id: chunk for chunk in chunks}

    for rc in relevant_chunks:
        original = chunk_map[rc.chunk_id]
        rc.chunk_text = original.text
        rc.page_no = original.page_no

    return PDFAnalysisResponse(
        filename=file.filename,
        paper_id=paper_id,
        pages=total_pages,
        chunk_count=len(chunks),
        relevant_chunks=relevant_chunks
    )
        
@router.post("/ask",response_model=PDFQAResponse)
async def ask_question(request:PDFQARequest):
    retrieved_chunks = search_chunks(
        query=request.question,
        paper_title=request.paper_title,
        k=10
    )

    qa_result = answer_question(chunks=retrieved_chunks,question=request.question)

    return PDFQAResponse(
        answer=qa_result.answer,
        confidence=qa_result.confidence,
        found_in_chunks=qa_result.found_in_chunks,
        found_in_pages=qa_result.found_in_pages
    )