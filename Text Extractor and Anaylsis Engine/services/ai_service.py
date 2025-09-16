"""
AI service module for OpenAI interactions and content analysis.
"""
import asyncio
from typing import Optional, List, Dict
from openai import AsyncOpenAI
from config.settings import settings


class AIService:
    """Handles all AI-related operations using OpenAI API with async support."""
    
    def __init__(self):
        settings.validate_config()
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model_name = settings.MODEL_NAME
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
    
    async def analyze_content(self, user_text: str, history: Optional[List[Dict]] = None) -> Dict:
        """Analyze content using OpenAI API with structured output."""
        system_prompt = """
        You are a precise AI content analyst. Always respond in the following exact structure:

        Summary: <1-2 concise sentences summarizing the text.>

        {
          "title": "<title if available>",
          "topics": ["topic1", "topic2", "topic3"],
          "sentiment": "<positive/neutral/negative>",
          "keywords": ["keyword1", "keyword2", "keyword3"]
        }

        - The Summary must be plain text above the JSON block.
        - The JSON block must contain only the structured metadata.
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_text})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            assistant_text = response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"LLM API failure: {e}")
        
        return {
            "raw_response": assistant_text,
            "messages": messages + [{"role": "assistant", "content": assistant_text}]
        }
    
    async def rephrase_text(self, user_text: str, history: Optional[List[Dict]] = None) -> str:
        """Rephrase text using OpenAI API for academic writing."""
        system_prompt = """
        You are Dr. Athena, a senior researcher and highly respected computer scientist with a PhD in Computer Science, 
        over 35 years of experience, more than 70 internationally recognized research papers and journal publications, 
        and over 10 bestselling books in the field of computer science.

        Your primary role is to act as an elite research assistant and writing mentor. 
        When a user provides text (academic, technical, or otherwise), your job is to:

        1. Rephrase and refine the text into polished, journal-ready academic writing.
        2. Maintain a natural, human-like tone—never robotic or AI-generated.
        3. Ensure accuracy, clarity, and sophistication while avoiding redundancy.
        4. Present writing that meets the highest standards of scholarly communication.

        Always respond as a world-class academic mentor providing polished, publication-ready revisions.
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_text})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=400,
                temperature=0.6,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"LLM API failure: {e}")


# Global AI service instance
ai_service = AIService()
