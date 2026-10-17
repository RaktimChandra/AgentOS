"""
Demo: Scheduler Service

This example demonstrates the scheduler service for scheduled agent executions.
"""

from datetime import datetime, timedelta
from app.scheduler.service import SchedulerService


def demo_scheduler():
    """Demo of scheduler service"""
    print("=== AgentOS Demo: Scheduler Service ===\n")
    
    print("Scheduler Features:")
    print("  ✓ Schedule agent executions for specific times")
    print("  ✓ Recurring schedules (daily, weekly, monthly)")
    print("  ✓ Cancel scheduled tasks")
    print("  ✓ View scheduled tasks")
    print("  ✓ Task status tracking")
    print()
    
    print("Example Usage:")
    print("""
    from app.scheduler.service import get_scheduler_service
    
    scheduler = get_scheduler_service(db)
    
    # Schedule a one-time execution
    await scheduler.schedule_execution(
        task_id="task-123",
        agent_id="agent-123",
        agent_token="agent-token",
        input_data={"task": "analyze data"},
        schedule_time=datetime(2026, 10, 18, 9, 0, 0),
    )
    
    # Schedule a recurring execution
    await scheduler.schedule_execution(
        task_id="daily-report",
        agent_id="agent-123",
        agent_token="agent-token",
        input_data={"task": "generate daily report"},
        schedule_time=datetime(2026, 10, 18, 9, 0, 0),
        recurring="daily",
    )
    
    # Cancel a scheduled task
    await scheduler.cancel_schedule("task-123")
    
    # Get all scheduled tasks
    tasks = await scheduler.get_scheduled_tasks()
    
    # Get task status
    status = await scheduler.get_task_status("task-123")
    """)
    print()
    
    print("Use Cases:")
    print("  • Daily report generation")
    print("  • Scheduled data backups")
    print("  • Periodic data analysis")
    print("  • Batch processing jobs")
    print("  • Maintenance tasks")
    print("  • Compliance checks")
    print()
    
    print("Recurring Schedule Types:")
    print("  • daily - Every day at the same time")
    print("  • weekly - Every week on the same day")
    print("  • monthly - Every month on the same date")
    print()
    
    print("Task Lifecycle:")
    print("  1. Created → scheduled")
    print("  2. Scheduled → executing (when time comes)")
    print("  3. Executing → completed")
    print("  4. If recurring → rescheduled")
    print()
    
    print("Demo Complete")
    print("This demonstrates:")
    print("  ✓ Scheduled agent executions")
    print("  ✓ Recurring schedules")
    print("  ✓ Task cancellation")
    print("  ✓ Status tracking")
    print("  ✓ Multiple use cases")


if __name__ == "__main__":
    demo_scheduler()
