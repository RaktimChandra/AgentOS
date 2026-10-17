"""Budget management for cost and resource controls"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.budget import Budget, BudgetType
from app.models.execution import Execution
import redis.asyncio as redis
from app.core.config import get_settings

settings = get_settings()


class BudgetManager:
    """Manager for budget tracking and enforcement"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = None
    
    async def _get_redis(self):
        """Get Redis client"""
        if self.redis_client is None:
            self.redis_client = redis.from_url(settings.REDIS_URL)
        return self.redis_client
    
    async def check_budget(
        self,
        budget_id: str,
        cost: float,
        tokens: int = 0,
    ) -> Dict[str, Any]:
        """
        Check if operation is within budget
        
        Args:
            budget_id: Budget ID
            cost: Cost of operation
            tokens: Token count
            
        Returns:
            Budget check result
        """
        # Get budget from database
        result = await self.db.execute(
            select(Budget).where(Budget.id == budget_id)
        )
        budget = result.scalar_one_or_none()
        
        if not budget:
            return {
                "allowed": False,
                "reason": "Budget not found",
            }
        
        # Check if within limit
        if budget.used + cost > budget.limit:
            return {
                "allowed": False,
                "reason": "Budget exceeded",
                "used": budget.used,
                "limit": budget.limit,
                "requested": cost,
            }
        
        # Check time window if applicable
        if budget.window_seconds:
            redis = await self._get_redis()
            window_key = f"budget:{budget_id}:window"
            
            # Get current window usage
            window_usage = await redis.get(window_key)
            window_usage = float(window_usage) if window_usage else 0.0
            
            if window_usage + cost > budget.limit:
                return {
                    "allowed": False,
                    "reason": "Time window budget exceeded",
                    "window_usage": window_usage,
                    "limit": budget.limit,
                }
        
        return {
            "allowed": True,
            "budget_id": budget_id,
            "remaining": budget.limit - budget.used,
        }
    
    async def record_usage(
        self,
        budget_id: str,
        cost: float,
        tokens: int = 0,
        execution_id: Optional[str] = None,
    ) -> bool:
        """
        Record budget usage
        
        Args:
            budget_id: Budget ID
            cost: Cost incurred
            tokens: Tokens used
            execution_id: Associated execution
            
        Returns:
            True if successful
        """
        # Update database
        await self.db.execute(
            update(Budget)
            .where(Budget.id == budget_id)
            .values(used=Budget.used + cost)
        )
        
        # Update time window if applicable
        result = await self.db.execute(
            select(Budget).where(Budget.id == budget_id)
        )
        budget = result.scalar_one_or_none()
        
        if budget and budget.window_seconds:
            redis = await self._get_redis()
            window_key = f"budget:{budget_id}:window"
            
            # Increment window usage
            await redis.incrbyfloat(window_key, cost)
            # Set expiry
            await redis.expire(window_key, budget.window_seconds)
        
        await self.db.commit()
        
        return True
    
    async def get_budget_status(
        self,
        budget_id: str,
    ) -> Dict[str, Any]:
        """
        Get current budget status
        
        Args:
            budget_id: Budget ID
            
        Returns:
            Budget status
        """
        result = await self.db.execute(
            select(Budget).where(Budget.id == budget_id)
        )
        budget = result.scalar_one_or_none()
        
        if not budget:
            return {"error": "Budget not found"}
        
        # Get window usage if applicable
        window_usage = None
        if budget.window_seconds:
            redis = await self._get_redis()
            window_key = f"budget:{budget_id}:window"
            window_usage = await redis.get(window_key)
            window_usage = float(window_usage) if window_usage else 0.0
        
        return {
            "budget_id": budget.id,
            "name": budget.name,
            "type": budget.budget_type,
            "limit": budget.limit,
            "used": budget.used,
            "remaining": budget.limit - budget.used,
            "utilization_percent": (budget.used / budget.limit * 100) if budget.limit > 0 else 0,
            "window_usage": window_usage,
            "rollover_enabled": budget.rollover_enabled,
        }
    
    async def create_budget(
        self,
        name: str,
        budget_type: BudgetType,
        limit: float,
        window_seconds: Optional[int] = None,
        rollover_enabled: bool = True,
    ) -> Budget:
        """
        Create a new budget
        
        Args:
            name: Budget name
            budget_type: Type of budget
            limit: Budget limit
            window_seconds: Time window in seconds (for rate limiting)
            rollover_enabled: Whether unused budget rolls over
            
        Returns:
            Created budget
        """
        import uuid
        
        budget = Budget(
            id=str(uuid.uuid4()),
            name=name,
            budget_type=budget_type,
            limit=limit,
            used=0.0,
            window_seconds=window_seconds,
            rollover_enabled=rollover_enabled,
        )
        
        self.db.add(budget)
        await self.db.commit()
        await self.db.refresh(budget)
        
        return budget
    
    async def reset_budget(
        self,
        budget_id: str,
    ) -> bool:
        """
        Reset budget usage to zero
        
        Args:
            budget_id: Budget ID
            
        Returns:
            True if successful
        """
        await self.db.execute(
            update(Budget)
            .where(Budget.id == budget_id)
            .values(used=0.0)
        )
        
        # Clear window usage
        redis = await self._get_redis()
        window_key = f"budget:{budget_id}:window"
        await redis.delete(window_key)
        
        await self.db.commit()
        
        return True
    
    async def check_agent_budget(
        self,
        agent_id: str,
        cost: float,
    ) -> Dict[str, Any]:
        """
        Check budget for a specific agent
        
        Args:
            agent_id: Agent ID
            cost: Cost to check
            
        Returns:
            Budget check result
        """
        from app.models.agent import Agent
        
        # Get agent's budget
        result = await self.db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        
        if not agent or not agent.budget_id:
            return {
                "allowed": False,
                "reason": "No budget configured for agent",
            }
        
        return await self.check_budget(agent.budget_id, cost)
    
    async def record_agent_usage(
        self,
        agent_id: str,
        cost: float,
        execution_id: Optional[str] = None,
    ) -> bool:
        """
        Record usage for an agent
        
        Args:
            agent_id: Agent ID
            cost: Cost incurred
            execution_id: Associated execution
            
        Returns:
            True if successful
        """
        from app.models.agent import Agent
        
        # Get agent's budget
        result = await self.db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        
        if not agent or not agent.budget_id:
            return False
        
        return await self.record_usage(agent.budget_id, cost, execution_id=execution_id)


# Global budget manager factory
def get_budget_manager(db: AsyncSession) -> BudgetManager:
    """Get budget manager instance"""
    return BudgetManager(db)
