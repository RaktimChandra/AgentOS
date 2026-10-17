"""Agent model"""

from sqlalchemy import Column, String, Integer, Text, Boolean, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base
from app.models.base import TimestampMixin


class AgentFramework(str, Enum):
    """Supported agent frameworks"""
    LANGCHAIN = "langchain"
    LANGGRAPH = "langgraph"
    AUTOGPT = "autogpt"
    CREWAI = "crewai"
    OPENAI_ASSISTANTS = "openai_assistants"
    ANTHROPIC_TOOL_USE = "anthropic_tool_use"
    CUSTOM = "custom"


class AgentStatus(str, Enum):
    """Agent deployment status"""
    DRAFT = "draft"
    DEPLOYED = "deployed"
    STOPPED = "stopped"
    ARCHIVED = "archived"


class Agent(Base, TimestampMixin):
    """Agent model"""
    
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    framework = Column(SQLEnum(AgentFramework), nullable=False)
    status = Column(SQLEnum(AgentStatus), default=AgentStatus.DRAFT, nullable=False)
    
    # Identity
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    trust_tier = Column(Integer, default=2, nullable=False)  # 0-5
    max_delegation_depth = Column(Integer, default=3, nullable=False)
    
    # Configuration
    config = Column(Text)  # JSON configuration
    code = Column(Text)  # Agent code
    tools = Column(Text)  # JSON array of tool IDs
    
    # Policy
    policy_id = Column(String, ForeignKey("policies.id"))
    
    # Budget
    budget_id = Column(String, ForeignKey("budgets.id"))
    
    # Deployment
    version = Column(Integer, default=1, nullable=False)
    deployed_at = Column(String)
    
    # Relationships
    owner = relationship("User", back_populates="agents")
    policy = relationship("Policy", back_populates="agents")
    budget = relationship("Budget", back_populates="agents")
    executions = relationship("Execution", back_populates="agent", cascade="all, delete-orphan")
