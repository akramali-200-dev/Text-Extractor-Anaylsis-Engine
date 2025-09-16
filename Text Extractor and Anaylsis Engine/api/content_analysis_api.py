"""
FastAPI application for content analysis and extraction.
"""
import asyncio
from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from config.settings import settings
from database.db_manager import db_manager
from services.ai_service import ai_service
from models.schemas import (
    AnalyzeRequest, AnalyzeBatchRequest, AnalyzeResponse,
    SearchRequest, SearchResponse, BatchAnalyzeResponse
)
from utils.text_processing import (
    extract_keywords, extract_json_and_summary, 
    compute_confidence, clean_text, validate_text_input
)


# Initialize FastAPI app
app = FastAPI(
    title="Content Analysis API",
    description="AI-powered content analysis and extraction service",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    await db_manager.init_database()


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    """Analyze content and return structured metadata."""
    text = clean_text(request.text)
    
    if not validate_text_input(text):
        raise HTTPException(status_code=400, detail="Empty text provided.")
    
    try:
        model_result = await ai_service.analyze_content(text)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    raw_response = model_result["raw_response"]
    summary, parsed = extract_json_and_summary(raw_response)
    
    # Extract metadata
    title = parsed.get("title") if parsed else None
    topics = parsed.get("topics", []) if parsed else []
    sentiment = parsed.get("sentiment", "neutral") if parsed else "neutral"
    keywords = parsed.get("keywords", extract_keywords(text)) if parsed else extract_keywords(text)
    confidence = compute_confidence(parsed, keywords)
    
    # Prepare record for database
    record = {
        "title": title,
        "topics": topics,
        "sentiment": sentiment,
        "keywords": keywords,
        "summary": summary,
        "content": text,
        "raw_response": raw_response,
        "messages": model_result["messages"],
        "created_at": datetime.utcnow().isoformat() + "Z",
        "confidence": confidence,
    }
    
    # Save to database
    row_id = await db_manager.save_analysis(record)
    
    return AnalyzeResponse(
        id=row_id,
        title=title,
        topics=topics,
        sentiment=sentiment,
        keywords=keywords,
        summary=summary,
        created_at=record["created_at"],
        confidence=confidence,
    )


@app.post("/analyze_batch", response_model=BatchAnalyzeResponse)
async def analyze_batch_endpoint(request: AnalyzeBatchRequest):
    """Analyze multiple texts in batch."""
    tasks = []
    
    for text in request.texts:
        task = analyze_single_text(text)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    processed_results = []
    for result in results:
        if isinstance(result, Exception):
            processed_results.append({"error": str(result)})
        else:
            processed_results.append(result.dict())
    
    return BatchAnalyzeResponse(count=len(processed_results), results=processed_results)


async def analyze_single_text(text: str):
    """Helper function to analyze a single text."""
    try:
        return await analyze_endpoint(AnalyzeRequest(text=text))
    except HTTPException as e:
        raise Exception(e.detail)


@app.get("/search", response_model=SearchResponse)
async def search_endpoint(topic: str = Query(...)):
    """Search analyses by topic or keyword."""
    topic = clean_text(topic)
    
    if not validate_text_input(topic):
        raise HTTPException(
            status_code=400, 
            detail="Provide a non-empty topic query parameter"
        )
    
    results = await db_manager.search_analyses_by_term(topic)
    return SearchResponse(count=len(results), results=results)


@app.get("/analysis/{analysis_id}")
async def get_analysis_by_id(analysis_id: int):
    """Get specific analysis by ID."""
    analysis = await db_manager.get_analysis_by_id(analysis_id)
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "content-analysis-api"}


async def test_api():
    """Manual smoke test for the API."""
    sample_text = "AI is transforming industries with generative models and large language models."
    
    try:
        response = await analyze_endpoint(AnalyzeRequest(text=sample_text))
        print("Test Passed:", response.dict())
        return True
    except Exception as e:
        print("Test Failed:", e)
        return False


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
