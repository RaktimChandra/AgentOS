"""Notification endpoints"""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import List
from app.core.security import get_current_user_id
from app.notifications.service import notification_service

router = APIRouter()


class NotificationCreate(BaseModel):
    """Notification creation request"""
    notification_type: str
    title: str
    message: str
    data: dict = {}


class NotificationResponse(BaseModel):
    """Notification response"""
    id: str
    type: str
    title: str
    message: str
    data: dict
    read: bool
    created_at: str


@router.post("/")
async def create_notification(
    notification_data: NotificationCreate,
    user_id: str = Depends(get_current_user_id),
):
    """Create a notification"""
    notification_id = await notification_service.create_notification(
        user_id=user_id,
        notification_type=notification_data.notification_type,
        title=notification_data.title,
        message=notification_data.message,
        data=notification_data.data,
    )
    
    return {"status": "created", "notification_id": notification_id}


@router.get("/")
async def get_notifications(
    unread_only: bool = Query(False),
    user_id: str = Depends(get_current_user_id),
):
    """Get user notifications"""
    notifications = await notification_service.get_user_notifications(
        user_id=user_id,
        unread_only=unread_only,
    )
    
    return {"notifications": notifications}


@router.get("/unread-count")
async def get_unread_count(user_id: str = Depends(get_current_user_id)):
    """Get unread notification count"""
    count = await notification_service.get_unread_count(user_id)
    return {"unread_count": count}


@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Mark notification as read"""
    success = await notification_service.mark_as_read(user_id, notification_id)
    
    if success:
        return {"status": "marked_as_read", "notification_id": notification_id}
    else:
        return {"status": "failed", "message": "Notification not found"}


@router.put("/read-all")
async def mark_all_as_read(user_id: str = Depends(get_current_user_id)):
    """Mark all notifications as read"""
    success = await notification_service.mark_all_as_read(user_id)
    
    if success:
        return {"status": "all_marked_as_read"}
    else:
        return {"status": "failed", "message": "No notifications found"}


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Delete a notification"""
    success = await notification_service.delete_notification(user_id, notification_id)
    
    if success:
        return {"status": "deleted", "notification_id": notification_id}
    else:
        return {"status": "failed", "message": "Notification not found"}
