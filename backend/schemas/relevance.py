from pydantic import BaseModel

class RelevantChunk(BaseModel):
    chunk_id:int
    chunk_text: str | None = None
    page_no:int|None = None
    relevance_score:int
    chunk_type:str
    reason:str
    suggested_use:str

class RelevanceResponse(BaseModel):
    evaluated_chunks:list[RelevantChunk]