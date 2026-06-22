from pydantic import BaseModel

class RAGSource(BaseModel):
    paper_title:str
    source:str
    url:str | None = None
    year:int | None = None
    relevance_score:float
    evidence_count:int

class RAGResponse(BaseModel):
    answer:str
    confidence:int
    papers_used:int
    key_findings: list[str]
    sources:list[RAGSource]

class RAGRequest(BaseModel):
    question:str
    paper_k:int = 5
    chunk_k:int = 5