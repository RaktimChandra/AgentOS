"""OPA Policy Engine integration"""

import httpx
from typing import Dict, Any, Optional
from app.core.config import get_settings

settings = get_settings()


class PolicyEngine:
    """OPA Policy Engine client"""
    
    def __init__(self):
        self.opa_url = settings.OPA_URL
        self.policy_path = settings.OPA_POLICY_PATH
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def evaluate(
        self,
        input_data: Dict[str, Any],
        policy_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate policy against input data
        
        Args:
            input_data: Input data for policy evaluation
            policy_path: Optional custom policy path
            
        Returns:
            Policy decision with allow/deny and reason
        """
        path = policy_path or self.policy_path
        url = f"{self.opa_url}/v1/data/{path}"
        
        try:
            response = await self.client.post(url, json={"input": input_data})
            response.raise_for_status()
            result = response.json()
            
            return {
                "allow": result.get("result", {}).get("allow", False),
                "reason": result.get("result", {}).get("reason", ""),
                "signals": result.get("result", {}).get("signals", {}),
            }
        except httpx.HTTPError as e:
            # Fail closed on errors
            return {
                "allow": False,
                "reason": f"Policy evaluation error: {str(e)}",
                "signals": {},
            }
    
    async def check_tool_authorization(
        self,
        agent: Dict[str, Any],
        tool: Dict[str, Any],
        action: str,
        args: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Check if agent is authorized to perform tool action
        
        Args:
            agent: Agent information (id, trust_tier, delegation_depth, etc.)
            tool: Tool information (name, min_trust_tier, max_delegation, etc.)
            action: Action to perform
            args: Action arguments
            context: Additional context (user, task, etc.)
            
        Returns:
            Authorization decision
        """
        input_data = {
            "agent": agent,
            "tool": tool,
            "action": action,
            "args": args,
            "context": context or {},
        }
        
        return await self.evaluate(input_data)
    
    async def check_budget(
        self,
        agent_id: str,
        cost: float,
        tokens: int,
        budget_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check if operation is within budget
        
        Args:
            agent_id: Agent ID
            cost: Cost of operation
            tokens: Token count
            budget_info: Budget information
            
        Returns:
            Budget check decision
        """
        input_data = {
            "agent_id": agent_id,
            "cost": cost,
            "tokens": tokens,
            "budget": budget_info,
        }
        
        return await self.evaluate(input_data, "agentos/budget")
    
    async def load_policy(self, rego_code: str, policy_path: str) -> bool:
        """
        Load a policy into OPA
        
        Args:
            rego_code: Rego policy code
            policy_path: Policy path in OPA
            
        Returns:
            True if successful
        """
        url = f"{self.opa_url}/v1/policies/{policy_path}"
        
        try:
            response = await self.client.put(url, content=rego_code)
            response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global policy engine instance
policy_engine = PolicyEngine()
