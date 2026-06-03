from pydantic import BaseModel

class RetrievalStats(BaseModel):
    total_papers: int
    unique_papers: int
    duplicate_papers_removed: int
    successful_sources: int
    failed_sources: int