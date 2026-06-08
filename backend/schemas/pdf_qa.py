from pydantic import BaseModel

class PDFQAResponse(BaseModel):
    answer:str
    confidence:int
    source_chunks:list[int]