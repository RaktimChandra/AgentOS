"""Agent management endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.identity.service import IdentityService
from app.models.agent import AgentFramework, AgentStatus

router = APIRouter()


class AgentCreate(BaseModel):
    """Agent creation request"""
    name: str
    framework: AgentFramework
    description: Optional[str] = None
    trust_tier: int = 2
    max_delegation_depth: int = 3
    config: Optional[Dict[str, Any]] = None
    code: Optional[str] = None


class AgentResponse(BaseModel):
    """Agent response"""
    id: str
    name: str
    description: Optional[str]
    framework: AgentFramework
    status: AgentStatus
    trust_tier: int
    max_delegation_depth: int
    owner_id: str


@router.post("/", response_model=AgentResponse)
async def create_agent(
    agent_data: AgentCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new agent"""
    identity_service = IdentityService(db)
    
    agent = await identity_service.create_agent(
        owner_id=user_id,
        name=agent_data.name,
        framework=agent_data.framework,
        description=agent_data.description,
        trust_tier=agent_data.trust_tier,
        max_delegation_depth=agent_data.max_delegation_depth,
        config=agent_data.config,
        code=agent_data.code,
    )
    
    return AgentResponse(
        id=agent.id,
        name=agent.name,
        description=agent.description,
        framework=agent.framework,
        status=agent.status,
        trust_tier=agent.trust_tier,
        max_delegation_depth=agent.max_delegation_depth,
        owner_id=agent.owner_id,
    )


@router.get("/")
async def list_agents(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List user's agents"""
    from sqlalchemy import select
    from app.models.agent import Agent
    
    result = await db.execute(
        select(Agent).where(Agent.owner_id == user_id)
    )
    agents = result.scalars().all()
    
    return [
        {
            "id": agent.id,
            "name": agent.name,
            "framework": agent.framework,
            "status": agent.status,
            "trust_tier": agent.trust_tier,
        }
        for agent in agents
    ]


@router.get("/{agent_id}")
async def get_agent(
    agent_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get agent details"""
    from sqlalchemy import select
    from app.models.agent import Agent
    
    result = await db.execute(
        select(Agent).where(
            Agent.id == agent_id,
            Agent.owner_id == user_id,
        )
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )
    
    return {
        "id": agent.id,
        "name": agent.name,
        "description": agent.description,
        "framework": agent.framework,
        "status": agent.status,
        "trust_tier": agent.trust_tier,
        "max_delegation_depth": agent.max_delegation_depth,
        "config": agent.config,
        "version": agent.version,
    }


@router.post("/{agent_id}/credentials")
async def get_agent_credentials(
    agent_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get agent credentials token"""
    from sqlalchemy import select
    from app.models.agent import Agent
    
    result = await db.execute(
        select(Agent).where(
            Agent.id == agent_id,
            Agent.owner_id == user_id,
        )
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )
    
    identity_service = IdentityService(db)
    token = await identity_service.create_agent_credentials(agent)
    
    return {"token": token}


@router.post("/{agent_id}/delegate")
async def delegate_to_subagent(
    agent_id: str,
    subagent_name: str,
    parent_token: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Delegate authority to a sub-agent"""
    from sqlalchemy import select
    from app.models.agent import Agent
    
    # Verify ownership
    result = await db.execute(
        select(Agent).where(
            Agent.id == agent_id,
            Agent.owner_id == user_id,
        )
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )
    
    identity_service = IdentityService(db)
    subagent_id, subagent_token = await identity_service.delegate_to_subagent(
        parent_agent_id=agent_id,
        parent_token=parent_token,
        subagent_name=subagent_name,
    )
    
    return {
        "subagent_id": subagent_id,
        "subagent_token": subagent_token,
    }
