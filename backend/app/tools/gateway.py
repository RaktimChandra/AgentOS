"""Tool gateway for intercepting and authorizing tool calls"""

from typing import Dict, Any, Optional
from app.policy.engine import policy_engine
from app.policy.signal_detector import SignalDetector
from app.execution.engine import tracer


class ToolGateway:
    """Gateway for intercepting and authorizing all tool calls"""
    
    def __init__(self):
        self.signal_detector = SignalDetector()
    
    async def execute_tool(
        self,
        agent_creds: Dict[str, Any],
        tool_name: str,
        action: str,
        args: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a tool with policy enforcement
        
        Args:
            agent_creds: Agent credentials
            tool_name: Tool name
            action: Action to perform
            args: Action arguments
            context: Additional context
            
        Returns:
            Tool execution result
        """
        from opentelemetry import trace
        
        with tracer.start_as_current_span("tool_gateway") as span:
            span.set_attribute("tool.name", tool_name)
            span.set_attribute("tool.action", action)
            
            # Detect signals
            args_str = str(args)
            signals = self.signal_detector.analyze_all(args_str)
            
            # Check for high-risk signals
            high_risk = any(s.get("severity") in ["high", "critical"] for s in signals)
            
            if high_risk:
                span.set_attribute("policy.decision", "deny")
                span.set_attribute("policy.reason", "High-risk signals detected")
                
                return {
                    "success": False,
                    "error": "High-risk signals detected",
                    "signals": signals,
                }
            
            # Get tool info
            tool_info = await self._get_tool_info(tool_name)
            
            # Check policy
            policy_decision = await policy_engine.check_tool_authorization(
                agent=agent_creds,
                tool=tool_info,
                action=action,
                args=args,
                context={**(context or {}), "signals": signals},
            )
            
            span.set_attribute("policy.decision", "allow" if policy_decision["allow"] else "deny")
            span.set_attribute("policy.reason", policy_decision.get("reason", ""))
            
            if not policy_decision["allow"]:
                return {
                    "success": False,
                    "error": policy_decision.get("reason", "Policy denied"),
                }
            
            # Execute tool
            result = await self._execute_tool_impl(tool_name, action, args)
            
            return {
                "success": True,
                "result": result,
            }
    
    async def _get_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """Get tool information"""
        # In production, this would query database
        tool_registry = {
            "database": {
                "name": "database",
                "min_trust_tier": 2,
                "max_delegation": 3,
            },
            "filesystem": {
                "name": "filesystem",
                "min_trust_tier": 1,
                "max_delegation": 5,
            },
            "http": {
                "name": "http",
                "min_trust_tier": 2,
                "max_delegation": 3,
            },
            "shell": {
                "name": "shell",
                "min_trust_tier": 4,
                "max_delegation": 2,
            },
        }
        
        return tool_registry.get(tool_name, {
            "name": tool_name,
            "min_trust_tier": 3,
            "max_delegation": 3,
        })
    
    async def _execute_tool_impl(
        self,
        tool_name: str,
        action: str,
        args: Dict[str, Any],
    ) -> Any:
        """Execute the actual tool implementation"""
        
        if tool_name == "database":
            return await self._execute_database(action, args)
        elif tool_name == "filesystem":
            return await self._execute_filesystem(action, args)
        elif tool_name == "http":
            return await self._execute_http(action, args)
        elif tool_name == "shell":
            return await self._execute_shell(action, args)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    async def _execute_database(self, action: str, args: Dict[str, Any]) -> Any:
        """Execute database tool"""
        # In production, this would execute actual database queries
        return {"query_result": "Executed"}
    
    async def _execute_filesystem(self, action: str, args: Dict[str, Any]) -> Any:
        """Execute filesystem tool"""
        # In production, this would perform actual file operations
        return {"file_result": "Executed"}
    
    async def _execute_http(self, action: str, args: Dict[str, Any]) -> Any:
        """Execute HTTP tool"""
        import httpx
        
        url = args.get("url")
        method = args.get("method", "GET")
        
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url)
            return {
                "status_code": response.status_code,
                "body": response.text,
            }
    
    async def _execute_shell(self, action: str, args: Dict[str, Any]) -> Any:
        """Execute shell tool"""
        # In production, this would execute in isolated environment
        command = args.get("command")
        return {"command_result": f"Executed: {command}"}


# Global tool gateway instance
tool_gateway = ToolGateway()
