"""
Database operations and models for the chatbot application.
"""
import aiosqlite
import json
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from config.settings import settings


class DatabaseManager:
    """Handles all database operations with async support."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.DB_PATH
    
    async def init_database(self) -> None:
        """Create database and tables if they don't exist."""
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    topics TEXT,
                    sentiment TEXT,
                    keywords TEXT,
                    summary TEXT,
                    content TEXT,
                    raw_response TEXT,
                    messages TEXT,
                    created_at TEXT,
                    confidence FLOAT
                )
                """
            )
            await conn.commit()
    
    async def save_analysis(self, record: Dict) -> int:
        """Save analysis record to database and return the row ID."""
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute(
                """
                INSERT INTO analyses
                (title, topics, sentiment, keywords, summary, content, raw_response, messages, created_at, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.get("title"),
                    json.dumps(record.get("topics", [])),
                    record.get("sentiment"),
                    json.dumps(record.get("keywords", [])),
                    record.get("summary"),
                    record.get("content"),
                    record.get("raw_response"),
                    json.dumps(record.get("messages", [])),
                    record.get("created_at"),
                    record.get("confidence"),
                ),
            )
            await conn.commit()
            return cursor.lastrowid
    
    async def search_analyses_by_term(self, term: str) -> List[Dict]:
        """Search analyses by term across multiple fields."""
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            q = "%" + term.lower() + "%"
            cursor = await conn.execute(
                """
                SELECT * FROM analyses
                WHERE lower(title) LIKE ?
                OR lower(topics) LIKE ?
                OR lower(keywords) LIKE ?
                OR lower(summary) LIKE ?
                OR lower(content) LIKE ?
                """,
                (q, q, q, q, q),
            )
            rows = await cursor.fetchall()
            result = []
            for r in rows:
                row = dict(r)
                try: 
                    row["topics"] = json.loads(row["topics"]) if row["topics"] else []
                except: 
                    row["topics"] = []
                try: 
                    row["keywords"] = json.loads(row["keywords"]) if row["keywords"] else []
                except: 
                    row["keywords"] = []
                try: 
                    row["messages"] = json.loads(row["messages"]) if row["messages"] else []
                except: 
                    row["messages"] = []
                result.append(row)
            return result
    
    async def get_analysis_by_id(self, analysis_id: int) -> Optional[Dict]:
        """Get analysis by ID."""
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,))
            row = await cursor.fetchone()
            
            if row:
                result = dict(row)
                try: 
                    result["topics"] = json.loads(result["topics"]) if result["topics"] else []
                except: 
                    result["topics"] = []
                try: 
                    result["keywords"] = json.loads(result["keywords"]) if result["keywords"] else []
                except: 
                    result["keywords"] = []
                try: 
                    result["messages"] = json.loads(result["messages"]) if result["messages"] else []
                except: 
                    result["messages"] = []
                return result
            return None


# Global database manager instance
db_manager = DatabaseManager()
