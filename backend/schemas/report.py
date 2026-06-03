from pydantic import BaseModel
from typing import Optional
from backend.schemas.stats import RetrievalStats

class SearchRequest(BaseModel):
    query: str
    project_description: Optional[str] = None   
    max_results_per_source: Optional[int] = 5
    sources: Optional[list[str]] = None           

class SourceReport(BaseModel):
    count: int
    status: str
    retrieval_type: str
    duration: float
    error: Optional[str]
    
class SearchResponse(BaseModel):
    query: str
    sources_requested: list[str]
    total_papers_retrieved: int
    total_ranked: int
    source_report: dict[str, SourceReport]
    retrieval_stats: dict[str, RetrievalStats]
    ranked_results: list
