"""Notification service for user alerts"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio


class NotificationService:
    """Service for managing user notifications"""
    
    def __init__(self):
        self.notifications: Dict[str, List[Dict[str, Any]]] = {}
    
    async def create_notification(
        self,
        user_id: str,
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create a notification for a user
        
        Args:
            user_id: User identifier
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            data: Additional data
            
        Returns:
            Notification ID
        """
        import uuid
        
        notification_id = str(uuid.uuid4())
        
        if user_id not in self.notifications:
            self.notifications[user_id] = []
        
        notification = {
            "id": notification_id,
            "type": notification_type,
            "title": title,
            "message": message,
            "data": data or {},
            "read": False,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        self.notifications[user_id].append(notification)
        
        return notification_id
    
    async def get_user_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Get notifications for a user
        
        Args:
            user_id: User identifier
            unread_only: Only return unread notifications
            
        Returns:
            List of notifications
        """
        if user_id not in self.notifications:
            return []
        
        notifications = self.notifications[user_id]
        
        if unread_only:
            notifications = [n for n in notifications if not n["read"]]
        
        return notifications
    
    async def mark_as_read(
        self,
        user_id: str,
        notification_id: str,
    ) -> bool:
        """
        Mark a notification as read
        
        Args:
            user_id: User identifier
            notification_id: Notification identifier
            
        Returns:
            True if successful
        """
        if user_id not in self.notifications:
            return False
        
        for notification in self.notifications[user_id]:
            if notification["id"] == notification_id:
                notification["read"] = True
                return True
        
        return False
    
    async def mark_all_as_read(self, user_id: str) -> bool:
        """
        Mark all notifications as read for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            True if successful
        """
        if user_id not in self.notifications:
            return False
        
        for notification in self.notifications[user_id]:
            notification["read"] = True
        
        return True
    
    async def delete_notification(
        self,
        user_id: str,
        notification_id: str,
    ) -> bool:
        """
        Delete a notification
        
        Args:
            user_id: User identifier
            notification_id: Notification identifier
            
        Returns:
            True if successful
        """
        if user_id not in self.notifications:
            return False
        
        self.notifications[user_id] = [
            n for n in self.notifications[user_id]
            if n["id"] != notification_id
        ]
        
        return True
    
    async def get_unread_count(self, user_id: str) -> int:
        """
        Get count of unread notifications for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            Count of unread notifications
        """
        if user_id not in self.notifications:
            return 0
        
        return sum(1 for n in self.notifications[user_id] if not n["read"])


# Global notification service instance
notification_service = NotificationService()
