"""Identity service for agent credentials and delegation"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserRole
from app.models.agent import Agent, AgentFramework, AgentStatus
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_agent_token,
    get_password_hash,
    verify_password,
)


class IdentityService:
    """Service for managing user and agent identities"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(
        self,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        role: UserRole = UserRole.DEVELOPER,
    ) -> User:
        """Create a new user"""
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            hashed_password=get_password_hash(password),
            full_name=full_name,
            role=role,
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> Optional[User]:
        """Authenticate a user"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    async def create_user_tokens(self, user: User) -> Dict[str, str]:
        """Create access and refresh tokens for user"""
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    
    async def create_agent(
        self,
        owner_id: str,
        name: str,
        framework: AgentFramework,
        description: Optional[str] = None,
        trust_tier: int = 2,
        max_delegation_depth: int = 3,
        config: Optional[Dict[str, Any]] = None,
        code: Optional[str] = None,
    ) -> Agent:
        """Create a new agent"""
        import json
        
        agent = Agent(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            framework=framework,
            status=AgentStatus.DRAFT,
            owner_id=owner_id,
            trust_tier=trust_tier,
            max_delegation_depth=max_delegation_depth,
            config=json.dumps(config) if config else None,
            code=code,
        )
        
        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)
        
        return agent
    
    async def create_agent_credentials(
        self,
        agent: Agent,
        delegation_depth: int = 0,
        expires_in_hours: int = 1,
    ) -> str:
        """Create agent credential token"""
        from app.models.user import User
        
        # Get owner
        result = await self.db.execute(
            select(User).where(User.id == agent.owner_id)
        )
        owner = result.scalar_one()
        
        # Determine capabilities based on trust tier
        capabilities = self._get_capabilities_for_tier(agent.trust_tier)
        
        # Create token
        token = create_agent_token(
            agent_id=agent.id,
            owner_id=owner.id,
            trust_tier=agent.trust_tier,
            delegation_depth=delegation_depth,
            max_delegation_depth=agent.max_delegation_depth,
            capabilities=capabilities,
            expires_delta=timedelta(hours=expires_in_hours),
        )
        
        return token
    
    def _get_capabilities_for_tier(self, trust_tier: int) -> list[str]:
        """Get allowed capabilities for trust tier"""
        tier_capabilities = {
            0: [],  # Untrusted - no capabilities
            1: ["read", "query"],  # Low trust - read only
            2: ["read", "query", "write"],  # Medium trust
            3: ["read", "query", "write", "delete"],  # High trust
            4: ["read", "query", "write", "delete", "admin"],  # Very high trust
            5: ["*"],  # Critical trust - full access
        }
        
        return tier_capabilities.get(trust_tier, [])
    
    async def delegate_to_subagent(
        self,
        parent_agent_id: str,
        parent_token: str,
        subagent_name: str,
    ) -> tuple[str, str]:
        """
        Delegate authority to a sub-agent
        
        Returns:
            Tuple of (subagent_id, subagent_token)
        """
        from app.core.security import decode_agent_token
        
        # Decode parent token
        parent_creds = decode_agent_token(parent_token)
        
        # Check delegation depth
        if parent_creds["delegation_depth"] >= parent_creds["max_delegation_depth"]:
            raise ValueError("Maximum delegation depth reached")
        
        # Get parent agent
        result = await self.db.execute(
            select(Agent).where(Agent.id == parent_agent_id)
        )
        parent_agent = result.scalar_one()
        
        # Create sub-agent with attenuated permissions
        sub_tier = max(0, parent_creds["trust_tier"] - 1)
        sub_agent = await self.create_agent(
            owner_id=parent_creds["owner_id"],
            name=subagent_name,
            framework=parent_agent.framework,
            trust_tier=sub_tier,
            max_delegation_depth=parent_creds["max_delegation_depth"],
        )
        
        # Create sub-agent credentials with incremented delegation depth
        sub_token = await self.create_agent_credentials(
            agent=sub_agent,
            delegation_depth=parent_creds["delegation_depth"] + 1,
        )
        
        return sub_agent.id, sub_token
    
    async def revoke_agent_credentials(self, agent_id: str) -> bool:
        """
        Revoke all credentials for an agent
        In production, this would add to a revocation list
        """
        # For now, we'll implement a simple revocation list in Redis
        import redis.asyncio as redis
        from app.core.config import get_settings
        
        settings = get_settings()
        redis_client = redis.from_url(settings.REDIS_URL)
        
        await redis_client.sadd("revoked_agents", agent_id)
        await redis_client.close()
        
        return True
    
    async def is_agent_revoked(self, agent_id: str) -> bool:
        """Check if agent credentials are revoked"""
        import redis.asyncio as redis
        from app.core.config import get_settings
        
        settings = get_settings()
        redis_client = redis.from_url(settings.REDIS_URL)
        
        is_revoked = await redis_client.sismember("revoked_agents", agent_id)
        await redis_client.close()
        
        return bool(is_revoked)
