"""Anthropic (Claude) integration for LLM-based agents"""

from typing import Dict, Any, Optional, List
from anthropic import AsyncAnthropic
from app.core.config import get_settings

settings = get_settings()


class AnthropicIntegration:
    """Anthropic API integration for agent LLM calls"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.client = AsyncAnthropic(api_key=self.api_key) if self.api_key else None
    
    async def message(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-opus-20240229",
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Generate message completion
        
        Args:
            messages: List of message dictionaries
            model: Model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Message result
        """
        if not self.client:
            raise ValueError("Anthropic API key not configured")
        
        # Convert messages to Claude format
        system_message = None
        claude_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                claude_messages.append(msg)
        
        response = await self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_message,
            messages=claude_messages,
        )
        
        return {
            "content": response.content[0].text,
            "model": response.model,
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
        }
    
    async def streaming_message(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-opus-20240229",
        max_tokens: int = 1000,
    ):
        """
        Generate streaming message completion
        
        Args:
            messages: List of message dictionaries
            model: Model to use
            max_tokens: Maximum tokens to generate
            
        Yields:
            Streaming text chunks
        """
        if not self.client:
            raise ValueError("Anthropic API key not configured")
        
        # Convert messages to Claude format
        system_message = None
        claude_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                claude_messages.append(msg)
        
        async with self.client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=system_message,
            messages=claude_messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text


# Global Anthropic integration instance
anthropic_integration = AnthropicIntegration()
