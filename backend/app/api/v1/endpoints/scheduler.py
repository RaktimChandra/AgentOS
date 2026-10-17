"""Scheduler endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.scheduler.service import get_scheduler_service

router = APIRouter()


class ScheduleCreate(BaseModel):
    """Schedule creation request"""
    task_id: str
    agent_id: str
    agent_token: str
    input_data: dict
    schedule_time: datetime
    recurring: Optional[str] = None


class ScheduleResponse(BaseModel):
    """Schedule response"""
    task_id: str
    status: str
    schedule_time: datetime


@router.post("/")
async def schedule_execution(
    schedule_data: ScheduleCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Schedule an agent execution"""
    scheduler = get_scheduler_service(db)
    
    success = await scheduler.schedule_execution(
        task_id=schedule_data.task_id,
        agent_id=schedule_data.agent_id,
        agent_token=schedule_data.agent_token,
        input_data=schedule_data.input_data,
        schedule_time=schedule_data.schedule_time,
        recurring=schedule_data.recurring,
    )
    
    if success:
        return {
            "status": "scheduled",
            "task_id": schedule_data.task_id,
            "schedule_time": schedule_data.schedule_time,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to schedule execution",
        )


@router.get("/")
async def list_schedules(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List all scheduled tasks"""
    scheduler = get_scheduler_service(db)
    tasks = await scheduler.get_scheduled_tasks()
    return {"tasks": tasks}


@router.get("/{task_id}")
async def get_schedule_status(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get status of a scheduled task"""
    scheduler = get_scheduler_service(db)
    task = await scheduler.get_task_status(task_id)
    
    if task:
        return task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.delete("/{task_id}")
async def cancel_schedule(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Cancel a scheduled execution"""
    scheduler = get_scheduler_service(db)
    success = await scheduler.cancel_schedule(task_id)
    
    if success:
        return {"status": "cancelled", "task_id": task_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
