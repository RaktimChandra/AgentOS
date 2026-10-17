"""Tests for identity service"""

import pytest
from app.identity.service import IdentityService
from app.models.user import UserRole
from app.models.agent import AgentFramework


class TestIdentityService:
    """Test identity service functionality"""
    
    @pytest.mark.asyncio
    async def test_create_user(self, db_session):
        """Test user creation"""
        service = IdentityService(db_session)
        
        user = await service.create_user(
            email="test@example.com",
            password="securepassword",
            full_name="Test User",
            role=UserRole.DEVELOPER,
        )
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.role == UserRole.DEVELOPER
        assert user.is_active is True
    
    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, db_session):
        """Test successful user authentication"""
        service = IdentityService(db_session)
        
        # Create user first
        await service.create_user(
            email="auth@example.com",
            password="password123",
        )
        
        # Authenticate
        user = await service.authenticate_user(
            email="auth@example.com",
            password="password123",
        )
        
        assert user is not None
        assert user.email == "auth@example.com"
    
    @pytest.mark.asyncio
    async def test_authenticate_user_failure(self, db_session):
        """Test failed user authentication"""
        service = IdentityService(db_session)
        
        # Create user first
        await service.create_user(
            email="auth@example.com",
            password="password123",
        )
        
        # Try wrong password
        user = await service.authenticate_user(
            email="auth@example.com",
            password="wrongpassword",
        )
        
        assert user is None
    
    @pytest.mark.asyncio
    async def test_create_agent(self, db_session):
        """Test agent creation"""
        service = IdentityService(db_session)
        
        # Create user first
        user = await service.create_user(
            email="agentowner@example.com",
            password="password",
        )
        
        # Create agent
        agent = await service.create_agent(
            owner_id=user.id,
            name="test-agent",
            framework=AgentFramework.LANGCHAIN,
            trust_tier=3,
        )
        
        assert agent.id is not None
        assert agent.name == "test-agent"
        assert agent.framework == AgentFramework.LANGCHAIN
        assert agent.trust_tier == 3
        assert agent.owner_id == user.id
    
    @pytest.mark.asyncio
    async def test_create_agent_credentials(self, db_session):
        """Test agent credential creation"""
        service = IdentityService(db_session)
        
        # Create user and agent
        user = await service.create_user(
            email="cred@example.com",
            password="password",
        )
        
        agent = await service.create_agent(
            owner_id=user.id,
            name="cred-agent",
            framework=AgentFramework.LANGCHAIN,
        )
        
        # Create credentials
        token = await service.create_agent_credentials(agent)
        
        assert token is not None
        assert isinstance(token, str)
