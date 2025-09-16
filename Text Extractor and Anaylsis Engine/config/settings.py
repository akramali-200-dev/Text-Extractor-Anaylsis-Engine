"""
Configuration settings for the chatbot application.
"""
import os
from typing import Optional


class Settings:
    """Application configuration settings."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "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")
    MODEL_NAME: str = "gpt-4o-mini"
    
    # Database Configuration
    DB_PATH: str = "extractor.db"
    
    # API Configuration
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_BASE_URL: str = f"http://{API_HOST}:{API_PORT}"
    
    # Analysis Configuration
    MAX_TOKENS: int = 700
    TEMPERATURE: float = 0.3
    MAX_KEYWORDS: int = 3
    
    # Text Processing Configuration
    MIN_WORD_LENGTH: int = 3
    
    @classmethod
    def validate_config(cls) -> None:
        """Validate required configuration settings."""
        if not cls.OPENAI_API_KEY:
            raise RuntimeError("Set OPENAI_API_KEY environment variable before running the application.")


# Global settings instance
settings = Settings()
