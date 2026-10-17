"""Replay system for deterministic execution replay"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from app.replay.recorder import replay_recorder
from app.execution.engine import tracer


class ReplayEngine:
    """Engine for replaying agent executions"""
    
    def __init__(self):
        self.recorder = replay_recorder
    
    async def full_replay(
        self,
        execution_id: str,
        agent_code: str,
        input_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Full replay: all boundaries from record (zero API calls)
        
        Args:
            execution_id: Execution to replay
            agent_code: Agent code to execute
            input_data: Input data
            
        Returns:
            Replay result
        """
        with tracer.start_as_current_span("full_replay") as span:
            span.set_attribute("execution.id", execution_id)
            span.set_attribute("replay.mode", "full")
            
            # Load recording
            recording = self.recorder.load_execution(execution_id)
            
            # Replay with all boundaries stubbed
            result = await self._replay_with_fixtures(
                agent_code=agent_code,
                input_data=input_data,
                fixtures=recording["fixtures"],
                cut_points=[],
            )
            
            return result
    
    async def cut_point_replay(
        self,
        execution_id: str,
        agent_code: str,
        input_data: Dict[str, Any],
        cut_points: List[str],
        boundary_handlers: Optional[Dict[str, Callable]] = None,
    ) -> Dict[str, Any]:
        """
        Cut-point replay: selected boundaries live, rest from record
        
        Args:
            execution_id: Execution to replay
            agent_code: Agent code to execute
            input_data: Input data
            cut_points: Boundary names to execute live
            boundary_handlers: Handlers for live boundaries
            
        Returns:
            Replay result
        """
        with tracer.start_as_current_span("cut_point_replay") as span:
            span.set_attribute("execution.id", execution_id)
            span.set_attribute("replay.mode", "cut_point")
            span.set_attribute("cut_points", cut_points)
            
            # Load recording
            recording = self.recorder.load_execution(execution_id)
            
            # Replay with cut-points live
            result = await self._replay_with_fixtures(
                agent_code=agent_code,
                input_data=input_data,
                fixtures=recording["fixtures"],
                cut_points=cut_points,
                boundary_handlers=boundary_handlers,
            )
            
            return result
    
    async def _replay_with_fixtures(
        self,
        agent_code: str,
        input_data: Dict[str, Any],
        fixtures: List[Dict[str, Any]],
        cut_points: List[str],
        boundary_handlers: Optional[Dict[str, Callable]] = None,
    ) -> Dict[str, Any]:
        """
        Replay agent with fixtures and cut-points
        
        Args:
            agent_code: Agent code
            input_data: Input data
            fixtures: Recorded fixtures
            cut_points: Boundaries to execute live
            boundary_handlers: Handlers for live boundaries
            
        Returns:
            Replay result
        """
        boundary_handlers = boundary_handlers or {}
        
        # Track call counts for guarded boundaries
        call_counts = {}
        
        # Replay execution
        output = None
        tool_calls = []
        
        for fixture in fixtures:
            boundary_type = fixture["boundary_type"]
            fixture_input = fixture["input"]
            
            # Track call count
            call_counts[boundary_type] = call_counts.get(boundary_type, 0) + 1
            
            # Check if this is a cut-point (execute live)
            if boundary_type in cut_points:
                # Execute live with handler
                if boundary_type in boundary_handlers:
                    result = await boundary_handlers[boundary_type](fixture_input)
                else:
                    # No handler provided, use default
                    result = await self._default_boundary_handler(boundary_type, fixture_input)
                
                # Verify call count if guarded
                if "call_count" in fixture.get("metadata", {}):
                    expected_count = fixture["metadata"]["call_count"]
                    if call_counts[boundary_type] > expected_count:
                        raise ValueError(
                            f"Boundary {boundary_type} called more times than expected: "
                            f"{call_counts[boundary_type]} > {expected_count}"
                        )
            else:
                # Use recorded fixture
                result = fixture["output"]
            
            tool_calls.append({
                "type": boundary_type,
                "input": fixture_input,
                "output": result,
                "from_fixture": boundary_type not in cut_points,
            })
        
        return {
            "output": output,
            "tool_calls": tool_calls,
            "call_counts": call_counts,
            "replayed_at": datetime.utcnow().isoformat(),
        }
    
    async def _default_boundary_handler(
        self,
        boundary_type: str,
        input_data: Any,
    ) -> Any:
        """Default handler for live boundaries"""
        # This would be implemented based on boundary type
        # For now, return a placeholder
        return f"Live execution of {boundary_type}"
    
    def compare_replay(
        self,
        original_result: Dict[str, Any],
        replay_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Compare original execution with replay
        
        Args:
            original_result: Original execution result
            replay_result: Replay execution result
            
        Returns:
            Comparison result
        """
        # Compare tool call sequences
        original_calls = original_result.get("tool_calls", [])
        replay_calls = replay_result.get("tool_calls", [])
        
        tools_changed = len(original_calls) != len(replay_calls)
        
        if not tools_changed:
            for i, (orig, replay) in enumerate(zip(original_calls, replay_calls)):
                if orig["type"] != replay["type"]:
                    tools_changed = True
                    break
        
        # Compare outputs
        output_changed = original_result.get("output") != replay_result.get("output")
        
        return {
            "tools_changed": tools_changed,
            "output_changed": output_changed,
            "regression_detected": tools_changed or output_changed,
            "original_call_count": len(original_calls),
            "replay_call_count": len(replay_calls),
        }


# Global replay engine instance
replay_engine = ReplayEngine()
