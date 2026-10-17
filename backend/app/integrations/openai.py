"""OpenAI integration for LLM-based agents"""

import os
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI
from app.core.config import get_settings

settings = get_settings()


class OpenAIIntegration:
    """OpenAI API integration for agent LLM calls"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> Dict[str, Any]:
        """
        Generate chat completion
        
        Args:
            messages: List of message dictionaries
            model: Model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Completion result
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "finish_reason": response.choices[0].finish_reason,
        }
    
    async def function_calling(
        self,
        messages: List[Dict[str, str]],
        functions: List[Dict[str, Any]],
        model: str = "gpt-4",
    ) -> Dict[str, Any]:
        """
        Generate completion with function calling
        
        Args:
            messages: List of message dictionaries
            functions: List of function definitions
            model: Model to use
            
        Returns:
            Completion result with function call
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        
        message = response.choices[0].message
        
        result = {
            "content": message.content,
            "function_call": None,
        }
        
        if message.function_call:
            result["function_call"] = {
                "name": message.function_call.name,
                "arguments": message.function_call.arguments,
            }
        
        return result
    
    async def embedding(
        self,
        text: str,
        model: str = "text-embedding-ada-002",
    ) -> List[float]:
        """
        Generate text embedding
        
        Args:
            text: Text to embed
            model: Embedding model
            
        Returns:
            Embedding vector
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        response = await self.client.embeddings.create(
            model=model,
            input=text,
        )
        
        return response.data[0].embedding
    
    async def moderation(
        self,
        text: str,
    ) -> Dict[str, Any]:
        """
        Check text for policy violations
        
        Args:
            text: Text to moderate
            
        Returns:
            Moderation result
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        response = await self.client.moderations.create(input=text)
        
        result = response.results[0]
        
        return {
            "flagged": result.flagged,
            "categories": result.categories,
            "category_scores": result.category_scores,
        }


# Global OpenAI integration instance
openai_integration = OpenAIIntegration()
