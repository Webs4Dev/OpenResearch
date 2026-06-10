from fastapi import APIRouter,UploadFile,File,Form
import fitz

from backend.pdf.parser import extract_pdf_pages
from backend.pdf.chunker import build_chunks_from_pages
from backend.agents.project_relevance_agent import sort_relevant_chunks
from backend.agents.pdf_qa_agent import answer_question
from backend.schemas.pdf_analysis import PDFAnalysisResponse
from backend.utils.logger import log

router = APIRouter()

@router.post("/pdf/analyze",response_model=PDFAnalysisResponse)

async def analyze_pdf(file:UploadFile=File(...),project_description:str=File(...),question:str=File(...)):

    temp_path=(
        f"temp_"
        f"{file.filename}"
    )
    contents=(await file.read())

    log(f"PDF uploaded: {file.filename}")
    with open(temp_path,"wb") as f:
        f.write(contents)

    pages=extract_pdf_pages(temp_path)
    log(f"Extracted pages from {file.filename}")

    chunks = build_chunks_from_pages(pages)
    log(f"Created {len(chunks)} chunks")

    text = "\n".join(page["text"] for page in pages)

    pages=len(fitz.open(temp_path))

    relevant_chunks = sort_relevant_chunks(chunks=chunks[:10],project_description=project_description,
        top_k=5)
    
    selected_chunks = [chunk for chunk in chunks if chunk.chunk_id in
        [   
            r.chunk_id
            for r in relevant_chunks
        ]
    ]

    qa_result = answer_question(question=question,chunks=selected_chunks)

    return PDFAnalysisResponse(
        filename=file.filename,
        pages=pages,
        text_length=len(text),
        chunk_count=len(chunks),
        relevant_chunks=relevant_chunks,
        answer=qa_result.answer,
        confidence=qa_result.confidence,
        found_in_chunks=qa_result.found_in_chunks,
        found_in_pages=qa_result.found_in_pages
    )