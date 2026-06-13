from pydantic import BaseModel

class RAGSource(BaseModel):
    paper_title:str
    source:str
    url:str | None = None

class RAGResponse(BaseModel):
    answer:str
    confidence:int
    sources:list[RAGSource]

class RAGRequest(BaseModel):
    question:str
    top_k:int = 5