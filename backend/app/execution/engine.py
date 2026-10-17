"""Agent execution engine with sandboxing and tracing"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from app.models.execution import Execution, ExecutionStatus
from app.models.trace import Trace
from app.policy.engine import policy_engine
from app.policy.signal_detector import SignalDetector
from app.core.config import get_settings

settings = get_settings()

# Initialize OpenTelemetry
tracer_provider = TracerProvider()
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer(__name__)


class ExecutionEngine:
    """Agent execution engine"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.signal_detector = SignalDetector()
    
    async def execute_agent(
        self,
        agent_id: str,
        agent_token: str,
        input_data: Dict[str, Any],
        timeout: int = None
    ) -> Dict[str, Any]:
        """
        Execute an agent with full tracing and policy enforcement
        
        Args:
            agent_id: Agent ID
            agent_token: Agent credential token
            input_data: Input data for execution
            timeout: Execution timeout in seconds
            
        Returns:
            Execution result
        """
        execution_id = str(uuid.uuid4())
        timeout = timeout or settings.DEFAULT_EXECUTION_TIMEOUT
        
        # Create execution record
        execution = Execution(
            id=execution_id,
            agent_id=agent_id,
            status=ExecutionStatus.RUNNING,
            input_data=str(input_data),
        )
        self.db.add(execution)
        await self.db.commit()
        
        # Start trace
        with tracer.start_as_current_span("execution") as span:
            span.set_attribute("execution.id", execution_id)
            span.set_attribute("agent.id", agent_id)
            
            try:
                # Execute with timeout
                result = await asyncio.wait_for(
                    self._execute_with_policy(
                        execution_id,
                        agent_id,
                        agent_token,
                        input_data,
                        span,
                    ),
                    timeout=timeout,
                )
                
                # Update execution
                execution.status = ExecutionStatus.COMPLETED
                execution.output_data = str(result)
                execution.duration_seconds = span.end_time - span.start_time
                
                await self.db.commit()
                
                return result
                
            except asyncio.TimeoutError:
                execution.status = ExecutionStatus.TIMEOUT
                execution.error_message = "Execution timeout"
                await self.db.commit()
                
                return {
                    "error": "Execution timeout",
                    "execution_id": execution_id,
                }
                
            except Exception as e:
                execution.status = ExecutionStatus.FAILED
                execution.error_message = str(e)
                await self.db.commit()
                
                return {
                    "error": str(e),
                    "execution_id": execution_id,
                }
    
    async def _execute_with_policy(
        self,
        execution_id: str,
        agent_id: str,
        agent_token: str,
        input_data: Dict[str, Any],
        parent_span,
    ) -> Dict[str, Any]:
        """Execute agent with policy enforcement at each boundary"""
        
        # Decode agent token
        from app.core.security import decode_agent_token
        agent_creds = decode_agent_token(agent_token)
        
        # Run agent execution (simplified for now)
        # In production, this would integrate with actual agent frameworks
        result = await self._run_agent_logic(
            agent_id,
            agent_creds,
            input_data,
            parent_span,
        )
        
        return result
    
    async def _run_agent_logic(
        self,
        agent_id: str,
        agent_creds: Dict[str, Any],
        input_data: Dict[str, Any],
        parent_span,
    ) -> Dict[str, Any]:
        """
        Run agent logic with tool call interception
        
        This is a simplified version. In production, this would:
        - Load agent code from database
- Execute in sandboxed environment
        - Intercept all tool calls
        - Enforce policy at each tool call
        """
        
        with tracer.start_as_current_span("agent_logic", parent=parent_span) as span:
            span.set_attribute("agent.id", agent_id)
            span.set_attribute("agent.trust_tier", agent_creds.get("trust_tier"))
            
            # Simulate agent execution
            # In production, this would be actual agent framework integration
            result = {
                "output": "Agent execution completed",
                "tool_calls": [],
                "tokens_used": 100,
            }
            
            return result
    
    async def intercept_tool_call(
        self,
        agent_creds: Dict[str, Any],
        tool_name: str,
        action: str,
        args: Dict[str, Any],
        parent_span,
    ) -> Dict[str, Any]:
        """
        Intercept and authorize tool calls
        
        Args:
            agent_creds: Agent credentials
            tool_name: Tool name
            action: Action to perform
            args: Action arguments
            parent_span: Parent span for tracing
            
        Returns:
            Tool call result or denial
        """
        with tracer.start_as_current_span("tool_call", parent=parent_span) as span:
            span.set_attribute("tool.name", tool_name)
            span.set_attribute("tool.action", action)
            
            # Detect signals in arguments
            args_str = str(args)
            signals = self.signal_detector.analyze_all(args_str)
            
            # Check policy
            tool_info = {
                "name": tool_name,
                "min_trust_tier": 2,
                "max_delegation": 3,
            }
            
            policy_decision = await policy_engine.check_tool_authorization(
                agent=agent_creds,
                tool=tool_info,
                action=action,
                args=args,
                context={"signals": signals},
            )
            
            span.set_attribute("policy.decision", "allow" if policy_decision["allow"] else "deny")
            span.set_attribute("policy.reason", policy_decision.get("reason", ""))
            
            if not policy_decision["allow"]:
                return {
                    "allowed": False,
                    "reason": policy_decision.get("reason", "Policy denied"),
                }
            
            # Execute tool call (simplified)
            # In production, this would call actual tool gateway
            return {
                "allowed": True,
                "result": f"Tool {tool_name} executed successfully",
            }
    
    async def stream_execution(
        self,
        agent_id: str,
        agent_token: str,
        input_data: Dict[str, Any],
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream execution results in real-time
        
        Args:
            agent_id: Agent ID
            agent_token: Agent credential token
            input_data: Input data for execution
            
        Yields:
            Execution updates
        """
        execution_id = str(uuid.uuid4())
        
        yield {
            "type": "start",
            "execution_id": execution_id,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Execute agent (simplified)
        yield {
            "type": "progress",
            "execution_id": execution_id,
            "message": "Processing...",
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        yield {
            "type": "complete",
            "execution_id": execution_id,
            "result": {"output": "Execution completed"},
            "timestamp": datetime.utcnow().isoformat(),
        }
