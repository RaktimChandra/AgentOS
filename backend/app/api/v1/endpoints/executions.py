"""Execution endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.execution.engine import ExecutionEngine

router = APIRouter()


class ExecutionCreate(BaseModel):
    """Execution request"""
    agent_id: str
    agent_token: str
    input_data: Dict[str, Any]
    timeout: Optional[int] = None


@router.post("/")
async def create_execution(
    execution_data: ExecutionCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Execute an agent"""
    execution_engine = ExecutionEngine(db)
    
    result = await execution_engine.execute_agent(
        agent_id=execution_data.agent_id,
        agent_token=execution_data.agent_token,
        input_data=execution_data.input_data,
        timeout=execution_data.timeout,
    )
    
    return result


@router.get("/{execution_id}")
async def get_execution(
    execution_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get execution details"""
    from sqlalchemy import select
    from app.models.execution import Execution
    
    result = await db.execute(
        select(Execution).where(Execution.id == execution_id)
    )
    execution = result.scalar_one_or_none()
    
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found",
        )
    
    return {
        "id": execution.id,
        "agent_id": execution.agent_id,
        "status": execution.status,
        "input_data": execution.input_data,
        "output_data": execution.output_data,
        "error_message": execution.error_message,
        "duration_seconds": execution.duration_seconds,
        "total_tokens": execution.total_tokens,
        "cost_usd": execution.cost_usd,
        "created_at": execution.created_at.isoformat(),
    }


@router.post("/{execution_id}/stream")
async def stream_execution(
    execution_data: ExecutionCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Stream execution results"""
    execution_engine = ExecutionEngine(db)
    
    async def event_generator():
        async for event in execution_engine.execute_agent(
            agent_id=execution_data.agent_id,
            agent_token=execution_data.agent_token,
            input_data=execution_data.input_data,
        ):
            yield f"data: {event}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
