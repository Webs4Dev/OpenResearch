from pydantic import BaseModel

class StoredChunk(BaseModel):
    paper_title:str
    source:str
    page_no:int
    chunk_id:int
    text:str