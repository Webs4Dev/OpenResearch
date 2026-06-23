from pydantic import BaseModel
from backend.schemas.relevance import RelevantChunk

class PDFAnalysisResponse_v1(BaseModel):
    filename:str
    pages:int
    text_length:int
    chunk_count:int
    relevant_chunks:list[RelevantChunk]
    answer:str
    confidence:int
    found_in_chunks:list[int]
    found_in_pages:list[int]

class PDFRequest(BaseModel):
    project_description:str
    question:str

class PDFIngestResponse(BaseModel):
    filename:str
    pages:int
    chunks_stored:int

class PDFAnalysisResponse(BaseModel):
    filename:str
    pages:int
    chunk_count:int
    relevant_chunks:list[RelevantChunk]

class PDFQARequest(BaseModel):
    paper_title: str
    question: str

class PDFQAResponse(BaseModel):
    answer:str
    confidence:int
    found_in_chunks:list[int]
    found_in_pages:list[int]