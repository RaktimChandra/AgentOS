"""
Demo: Notification Service

This example demonstrates the notification service for user alerts.
"""

from app.notifications.service import notification_service


def demo_notifications():
    """Demo of notification service"""
    print("=== AgentOS Demo: Notification Service ===\n")
    
    print("Notification Features:")
    print("  ✓ Create notifications for users")
    print("  ✓ Mark notifications as read")
    print("  ✓ Mark all notifications as read")
    print("  ✓ Delete notifications")
    print("  ✓ Get unread count")
    print("  ✓ Filter by read status")
    print()
    
    print("Example Usage:")
    print("""
    from app.notifications.service import notification_service
    
    # Create a notification
    notification_id = await notification_service.create_notification(
        user_id="user-123",
        notification_type="agent_execution_completed",
        title="Agent Execution Completed",
        message="Your agent 'data-analyzer' completed successfully",
        data={"agent_id": "agent-123", "execution_id": "exec-456"},
    )
    
    # Get all notifications
    notifications = await notification_service.get_user_notifications(
        user_id="user-123",
    )
    
    # Get only unread notifications
    unread = await notification_service.get_user_notifications(
        user_id="user-123",
        unread_only=True,
    )
    
    # Mark as read
    await notification_service.mark_as_read(
        user_id="user-123",
        notification_id=notification_id,
    )
    
    # Mark all as read
    await notification_service.mark_all_as_read(user_id="user-123")
    
    # Get unread count
    count = await notification_service.get_unread_count(user_id="user-123")
    
    # Delete notification
    await notification_service.delete_notification(
        user_id="user-123",
        notification_id=notification_id,
    )
    """)
    print()
    
    print("Notification Types:")
    print("  • agent_execution_completed")
    print("  • agent_execution_failed")
    print("  • policy_denied")
    print("  • signal_detected")
    print("  • budget_exceeded")
    print("  • system_alert")
    print("  • maintenance_scheduled")
    print()
    
    print("Use Cases:")
    print("  • Alert users about agent failures")
    print("  • Notify about policy violations")
    print("  • Warn about budget limits")
    print("  • System maintenance notifications")
    print("  • Security alerts")
    print("  • Execution completion notifications")
    print()
    
    print("Notification Channels (Future):")
    print("  • In-app notifications")
    print("  • Email notifications")
    print("  • SMS notifications")
    print("  • Push notifications")
    print("  • Slack/Discord integration")
    print()
    
    print("Demo Complete")
    print("This demonstrates:")
    print("  ✓ Notification creation")
    print("  ✓ Read/unread tracking")
    print("  ✓ Notification filtering")
    print("  ✓ Bulk operations")
    print("  ✓ Deletion")
    print("  ✓ Multiple notification types")
