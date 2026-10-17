"""Analytics endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.core.database import get_db
from app.core.security import get_current_user_id
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/overview")
async def get_analytics_overview(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get analytics overview"""
    # This would query the database for actual analytics
    # For now, return a simulated response
    return {
        "period": "last_7_days",
        "agent_executions": {
            "total": 1234,
            "successful": 1180,
            "failed": 54,
            "success_rate": 0.956,
        },
        "policy_evaluations": {
            "total": 5678,
            "allowed": 5432,
            "denied": 246,
            "allow_rate": 0.957,
        },
        "tool_calls": {
            "total": 8901,
            "authorized": 8756,
            "denied": 145,
            "authorization_rate": 0.984,
        },
        "signal_detections": {
            "total": 234,
            "high_severity": 12,
            "medium_severity": 89,
            "low_severity": 133,
        },
        "budget_utilization": {
            "total_budget": 1000.0,
            "used": 756.50,
            "remaining": 243.50,
            "utilization_percent": 75.65,
        },
    }


@router.get("/executions/trend")
async def get_execution_trend(
    days: int = 30,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get execution trend over time"""
    # Simulated trend data
    return {
        "period_days": days,
        "trend": [
            {"date": "2026-10-01", "count": 45, "success_rate": 0.95},
            {"date": "2026-10-02", "count": 52, "success_rate": 0.94},
            {"date": "2026-10-03", "count": 48, "success_rate": 0.96},
            {"date": "2026-10-04", "count": 61, "success_rate": 0.97},
            {"date": "2026-10-05", "count": 55, "success_rate": 0.95},
        ],
    }


@router.get("/policy/decisions")
async def get_policy_decision_distribution(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get policy decision distribution"""
    return {
        "total_evaluations": 5678,
        "decisions": {
            "allow": 5432,
            "deny": 246,
        },
        "by_reason": {
            "trust_tier_insufficient": 89,
            "delegation_depth_exceeded": 45,
            "signal_detected": 67,
            "budget_exceeded": 23,
            "other": 22,
        },
    }


@router.get("/tools/usage")
async def get_tool_usage_stats(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get tool usage statistics"""
    return {
        "total_calls": 8901,
        "by_tool": {
            "database": 3456,
            "filesystem": 2345,
            "http": 1890,
            "shell": 567,
            "calculator": 643,
        },
        "authorization_rate": {
            "database": 0.98,
            "filesystem": 0.95,
            "http": 0.99,
            "shell": 0.85,
            "calculator": 1.0,
        },
    }


@router.get("/signals/distribution")
async def get_signal_distribution(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get signal detection distribution"""
    return {
        "total_detections": 234,
        "by_type": {
            "pii": 45,
            "secrets": 23,
            "sql_injection": 12,
            "command_injection": 8,
            "prompt_injection": 34,
            "path_traversal": 15,
            "xss": 18,
            "intent_drift": 56,
            "cost_spike": 12,
            "runaway_loop": 11,
        },
        "by_severity": {
            "high": 12,
            "medium": 89,
            "low": 133,
        },
    }
