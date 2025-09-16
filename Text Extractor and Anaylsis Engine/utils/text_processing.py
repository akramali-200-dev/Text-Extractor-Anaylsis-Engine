"""
Utility functions for text processing and analysis.
"""
import re
import json
from typing import List, Tuple, Optional
from config.settings import settings


# Common English stopwords
STOPWORDS = {
    "the", "and", "is", "in", "it", "of", "to", "a", "for", "on", "with", "that", "this",
    "as", "are", "be", "by", "an", "from", "or", "at", "was", "which", "has", "have"
}


def extract_keywords(text: str, top_n: int = None) -> List[str]:
    """Extract keywords from text using simple frequency analysis."""
    if top_n is None:
        top_n = settings.MAX_KEYWORDS
    
    tokens = re.split(r'[^A-Za-z]+', text.lower())
    counts = {}
    
    for token in tokens:
        if not token or len(token) < settings.MIN_WORD_LENGTH or token in STOPWORDS:
            continue
        counts[token] = counts.get(token, 0) + 1
    
    sorted_tokens = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [token for token, _ in sorted_tokens[:top_n]]


def extract_json_and_summary(text: str) -> Tuple[Optional[str], Optional[dict]]:
    """Extract summary and JSON object from AI response text."""
    summary = None
    json_obj = None
    
    # Extract summary
    summary_match = re.search(r"Summary:\s*(.+?)(?:\n\s*\{|$)", text, re.S)
    if summary_match:
        summary = summary_match.group(1).strip()
    
    # Extract JSON
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1:
        try:
            json_obj = json.loads(text[start:end+1])
        except json.JSONDecodeError:
            pass
    
    return summary, json_obj


def compute_confidence(parsed: Optional[dict], keywords: List[str]) -> float:
    """Compute confidence score for analysis results."""
    score = 0.0
    
    if parsed:
        score += 0.4
    if keywords:
        score += 0.3
    if parsed and parsed.get("sentiment"):
        score += 0.1
    if parsed and parsed.get("topics"):
        score += 0.2
    
    return round(score, 2)


def clean_text(text: str) -> str:
    """Clean and normalize input text."""
    return text.strip()


def validate_text_input(text: str) -> bool:
    """Validate text input for analysis."""
    cleaned_text = clean_text(text)
    return len(cleaned_text) > 0
