from fastapi import APIRouter,UploadFile,File
import fitz

from backend.pdf.parser import extract_pdf_text
from backend.pdf.chunker import build_chunks
from backend.utils.logger import log
from backend.schemas.pdf import PDFAnalysisResponse

router = APIRouter()

@router.post(
    "/pdf/analyze",

    response_model=
    PDFAnalysisResponse
)

async def analyze_pdf(file:UploadFile=File(...)):

    temp_path=(
        f"temp_"
        f"{file.filename}"
    )
    contents=(await file.read())

    with open(temp_path,"wb") as f:
        f.write(contents)

    text=extract_pdf_text(temp_path)
    log(f"Extracted text from {file.filename}")

    chunks = build_chunks(text)
    log(f"Created {len(chunks)} chunks")

    pages=len(fitz.open(temp_path))

    return PDFAnalysisResponse(
        filename=file.filename,
        pages=pages,
        text_length=len(text),
        extracted_text=text,
        chunk_count=len(chunks)
    )