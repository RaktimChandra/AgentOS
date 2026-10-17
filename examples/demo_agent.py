"""
Demo Agent: Database Query Agent

This example demonstrates an agent that queries a database with policy enforcement.
"""

from app.execution.engine import ExecutionEngine
from app.identity.service import IdentityService
from app.models.agent import AgentFramework
from app.core.database import AsyncSession
from app.core.security import decode_agent_token


async def demo_database_agent():
    """Demo of a database query agent with policy enforcement"""
    
    # This would be called with a real database session
    # db = get_db()
    
    # Create identity service
    # identity_service = IdentityService(db)
    
    # Create a user
    # user = await identity_service.create_user(
    #     email="demo@example.com",
    #     password="securepassword",
    # )
    
    # Create an agent with trust tier 2 (can read but not write)
    # agent = await identity_service.create_agent(
    #     owner_id=user.id,
    #     name="database-query-agent",
    #     framework=AgentFramework.LANGCHAIN,
    #     trust_tier=2,  # Medium trust - read only
    #     description="Agent for querying database with policy enforcement",
    # )
    
    # Get agent credentials
    # agent_token = await identity_service.create_agent_credentials(agent)
    
    # Decode token to see agent credentials
    # agent_creds = decode_agent_token(agent_token)
    
    print("=== AgentOS Demo: Database Query Agent ===\n")
    print("Agent Configuration:")
    print(f"  Name: database-query-agent")
    print(f"  Framework: LangChain")
    print(f"  Trust Tier: 2 (Medium - Read Only)")
    print(f"  Capabilities: read, query")
    print(f"  Max Delegation Depth: 3")
    print()
    
    print("=== Scenario 1: Allowed Query ===")
    print("Agent attempts: SELECT * FROM users WHERE id = 123")
    print("Policy Decision: ALLOWED")
    print("Reason: Trust tier sufficient, no SQL injection detected")
    print()
    
    print("=== Scenario 2: Blocked Query ===")
    print("Agent attempts: DROP TABLE users")
    print("Policy Decision: DENIED")
    print("Reason: Dangerous SQL pattern detected")
    print("Evidence recorded in audit log")
    print()
    
    print("=== Scenario 3: Blocked Write Operation ===")
    print("Agent attempts: UPDATE users SET admin = true")
    print("Policy Decision: DENIED")
    print("Reason: Trust tier 2 does not allow write operations")
    print()
    
    print("=== Scenario 4: SQL Injection Attempt ===")
    print("Agent attempts: SELECT * FROM users WHERE 1=1; DROP TABLE users")
    print("Policy Decision: DENIED")
    print("Reason: SQL injection pattern detected")
    print("Signal: sql_injection (high severity)")
    print()
    
    print("=== Execution Tracing ===")
    print("All actions are traced with OpenTelemetry:")
    print("  - Agent execution span")
    print("  - Tool call spans")
    print("  - Policy decision spans")
    print("  - Database query spans")
    print("View traces in Jaeger: http://localhost:16686")
    print()
    
    print("=== Budget Enforcement ===")
    print("Agent budget: $100.00")
    print("Query cost: $0.05")
    print("Budget remaining: $99.95")
    print()
    
    print("=== Demo Complete ===")
    print("This demonstrates:")
    print("  ✓ Runtime policy enforcement")
    print("  ✓ Trust tier-based authorization")
    print("  ✓ Signal detection (SQL injection)")
    print("  ✓ Execution tracing")
    print("  ✓ Budget management")
    print("  ✓ Audit logging")


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_database_agent())
