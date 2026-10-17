"""Scheduler service for scheduled agent executions"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio
import json


class SchedulerService:
    """Service for scheduling agent executions"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.scheduled_tasks: Dict[str, Dict[str, Any]] = {}
        self.running = False
    
    async def schedule_execution(
        self,
        task_id: str,
        agent_id: str,
        agent_token: str,
        input_data: Dict[str, Any],
        schedule_time: datetime,
        recurring: Optional[str] = None,  # "daily", "weekly", "monthly"
    ) -> bool:
        """
        Schedule an agent execution
        
        Args:
            task_id: Task identifier
            agent_id: Agent to execute
            agent_token: Agent credentials
            input_data: Input for execution
            schedule_time: When to execute
            recurring: Recurring schedule (optional)
            
        Returns:
            True if scheduled successfully
        """
        self.scheduled_tasks[task_id] = {
            "agent_id": agent_id,
            "agent_token": agent_token,
            "input_data": input_data,
            "schedule_time": schedule_time,
            "recurring": recurring,
            "status": "scheduled",
            "created_at": datetime.utcnow(),
        }
        
        return True
    
    async def cancel_schedule(self, task_id: str) -> bool:
        """
        Cancel a scheduled execution
        
        Args:
            task_id: Task identifier
            
        Returns:
            True if cancelled successfully
        """
        if task_id in self.scheduled_tasks:
            del self.scheduled_tasks[task_id]
            return True
        return False
    
    async def get_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """Get all scheduled tasks"""
        return list(self.scheduled_tasks.values())
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a scheduled task"""
        return self.scheduled_tasks.get(task_id)
    
    async def start_scheduler(self):
        """Start the scheduler loop"""
        self.running = True
        
        while self.running:
            now = datetime.utcnow()
            
            # Check for tasks to execute
            for task_id, task in list(self.scheduled_tasks.items()):
                if task["schedule_time"] <= now and task["status"] == "scheduled":
                    # Execute the task
                    await self._execute_task(task_id, task)
                    
                    # Handle recurring tasks
                    if task["recurring"]:
                        await self._reschedule_recurring(task_id, task)
            
            # Sleep for 1 second
            await asyncio.sleep(1)
    
    async def _execute_task(self, task_id: str, task: Dict[str, Any]):
        """Execute a scheduled task"""
        # This would call the execution engine
        task["status"] = "executing"
        task["executed_at"] = datetime.utcnow()
        
        # Simulate execution
        await asyncio.sleep(1)
        
        task["status"] = "completed"
        task["completed_at"] = datetime.utcnow()
    
    async def _reschedule_recurring(self, task_id: str, task: Dict[str, Any]):
        """Reschedule a recurring task"""
        if task["recurring"] == "daily":
            task["schedule_time"] = task["schedule_time"] + timedelta(days=1)
        elif task["recurring"] == "weekly":
            task["schedule_time"] = task["schedule_time"] + timedelta(weeks=1)
        elif task["recurring"] == "monthly":
            # Approximate month
            task["schedule_time"] = task["schedule_time"] + timedelta(days=30)
        
        task["status"] = "scheduled"
    
    async def stop_scheduler(self):
        """Stop the scheduler loop"""
        self.running = False


# Global scheduler service factory
def get_scheduler_service(db: AsyncSession) -> SchedulerService:
    """Get scheduler service instance"""
    return SchedulerService(db)
