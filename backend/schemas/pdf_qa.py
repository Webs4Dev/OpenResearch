from pydantic import BaseModel

class PDFQAResponse(BaseModel):
    answer:str
    confidence:int
    found_in_chunks:list[int]