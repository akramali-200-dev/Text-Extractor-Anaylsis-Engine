"""
Pydantic models for data validation and API schemas.
"""
from typing import Optional, List
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    """Request model for content analysis."""
    text: str


class AnalyzeBatchRequest(BaseModel):
    """Request model for batch content analysis."""
    texts: List[str]


class AnalyzeResponse(BaseModel):
    """Response model for content analysis."""
    id: int
    title: Optional[str]
    topics: List[str] = []
    sentiment: Optional[str]
    keywords: List[str] = []
    summary: Optional[str]
    created_at: str
    confidence: float


class SearchRequest(BaseModel):
    """Request model for search operations."""
    topic: str


class SearchResponse(BaseModel):
    """Response model for search operations."""
    count: int
    results: List[dict]


class BatchAnalyzeResponse(BaseModel):
    """Response model for batch analysis operations."""
    count: int
    results: List[dict]
