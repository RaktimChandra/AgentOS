"""
Demo: LLM Integration

This example demonstrates OpenAI and Anthropic integration for agent LLM calls.
"""

import asyncio
from app.integrations.openai import OpenAIIntegration
from app.integrations.anthropic import AnthropicIntegration


def demo_openai_integration():
    """Demo of OpenAI integration"""
    print("=== AgentOS Demo: OpenAI Integration ===\n")
    
    # Note: This requires OPENAI_API_KEY to be set in .env
    print("OpenAI Integration Features:")
    print("  ✓ Chat completion (GPT-4, GPT-3.5)")
    print("  ✓ Function calling")
    print("  ✓ Text embedding (Ada-002)")
    print("  ✓ Content moderation")
    print("  ✓ Streaming responses")
    print()
    
    print("Example Usage:")
    print("""
    from app.integrations.openai import openai_integration
    
    # Chat completion
    result = await openai_integration.chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ],
        model="gpt-4",
    )
    
    # Function calling
    result = await openai_integration.function_calling(
        messages=[...],
        functions=[
            {
                "name": "get_weather",
                "description": "Get current weather",
                "parameters": {...},
            }
        ],
    )
    
    # Embedding
    embedding = await openai_integration.embedding(
        text="Hello, world!",
        model="text-embedding-ada-002",
    )
    
    # Moderation
    moderation = await openai_integration.moderation(
        text="Check this content for policy violations",
    )
    """)
    print()
    
    print("Use Cases:")
    print("  • Agent reasoning and decision making")
    print("  • Natural language understanding")
    print("  • Code generation and analysis")
    print("  • Content safety checks")
    print("  • Semantic search with embeddings")
    print()


def demo_anthropic_integration():
    """Demo of Anthropic integration"""
    print("=== AgentOS Demo: Anthropic (Claude) Integration ===\n")
    
    # Note: This requires ANTHROPIC_API_KEY to be set in .env
    print("Anthropic Integration Features:")
    print("  ✓ Message completion (Claude 3 Opus, Sonnet, Haiku)")
    print("  ✓ Streaming responses")
    print("  ✓ Long context windows (200K tokens)")
    print("  ✓ Constitutional AI principles")
    print("  ✓ Vision capabilities")
    print()
    
    print("Example Usage:")
    print("""
    from app.integrations.anthropic import anthropic_integration
    
    # Message completion
    result = await anthropic_integration.message(
        messages=[
            {"role": "user", "content": "Hello!"},
        ],
        model="claude-3-opus-20240229",
    )
    
    # Streaming
    async for chunk in anthropic_integration.streaming_message(
        messages=[...],
        model="claude-3-opus-20240229",
    ):
        print(chunk, end="")
    """)
    print()
    
    print("Use Cases:")
    print("  • Complex reasoning tasks")
    print("  • Long document analysis")
    print("  • Code review and generation")
    print("  • Research and analysis")
    print("  • Constitutional AI for safety")
    print()


def demo_combined_usage():
    """Demo of combined LLM usage"""
    print("=== AgentOS Demo: Combined LLM Usage ===\n")
    
    print("Multi-LLM Strategy:")
    print("  • Use GPT-4 for general tasks")
    print("  • Use Claude for complex reasoning")
    print("  • Use GPT-3.5 for simple tasks (cost savings)")
    print("  • Use embeddings for semantic search")
    print("  • Use moderation for safety")
    print()
    
    print("Cost Optimization:")
    print("  • Route simple queries to cheaper models")
    print("  • Cache LLM responses")
    print("  • Use streaming for long responses")
    print("  • Monitor token usage")
    print("  • Set budget limits per agent")
    print()
    
    print("Safety Layers:")
    print("  1. Input validation")
    print("  2. Content moderation")
    print("  3. Policy enforcement")
    print("  4. Signal detection")
    print("  5. Output filtering")
    print()
    
    print("Demo Complete")
    print("This demonstrates:")
    print("  ✓ OpenAI integration (GPT-4, GPT-3.5)")
    print("  ✓ Anthropic integration (Claude 3)")
    print("  ✓ Function calling")
    print("  ✓ Embeddings")
    print("  ✓ Content moderation")
    print("  ✓ Streaming responses")
    print("  ✓ Multi-LLM strategy")
    print("  ✓ Cost optimization")
    print("  ✓ Safety layers")


if __name__ == "__main__":
    demo_openai_integration()
    demo_anthropic_integration()
    demo_combined_usage()
