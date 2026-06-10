from pydantic import BaseModel

class PDFChunk(BaseModel):
    chunk_id:int
    page_no:int
    text:str
    length:int