from pydantic import BaseModel
from backend.schemas.relevance import RelevantChunk

class PDFAnalysisResponse(BaseModel):
    filename:str
    pages:int
    text_length:int
    chunk_count:int
    relevant_chunks:list[RelevantChunk]
    answer:str
    confidence:int
    found_in_chunks:list[int]

class PDFRequest(BaseModel):
    project_description:str
    question:str