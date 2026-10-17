"""Monitoring and metrics endpoints"""

from fastapi import APIRouter, Depends
from prometheus_client import generate_latest
from app.core.security import get_current_user_id

router = APIRouter()


@router.get("/metrics")
async def get_metrics(user_id: str = Depends(get_current_user_id)):
    """Get Prometheus metrics"""
    from prometheus_client import CONTENT_TYPE_LATEST
    from fastapi import Response
    
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0",
    }


@router.get("/stats")
async def get_stats(user_id: str = Depends(get_current_user_id)):
    """Get system statistics"""
    from app.monitoring.metrics import (
        agent_executions_total,
        policy_evaluations_total,
        tool_calls_total,
        active_agents,
        active_policies,
    )
    
    return {
        "agent_executions": agent_executions_total._value.get(),
        "policy_evaluations": policy_evaluations_total._value.get(),
        "tool_calls": tool_calls_total._value.get(),
        "active_agents": active_agents._value.get(),
        "active_policies": active_policies._value.get(),
    }
