from pydantic import BaseModel

class PDFChunk(BaseModel):
    chunk_id:int
    text:str
    length:int