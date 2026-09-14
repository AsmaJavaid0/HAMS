from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Notification, User
from app.schemas import NotificationCreate, NotificationUpdate, NotificationResponse
from app.dependencies import get_current_user
from app.services.notification import NotificationService

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"],
)

notification_service = NotificationService()


@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    skip: int = 0,
    limit: int = 100,
    is_read: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get current user ID
    user_id = current_user["user"].id

    if is_read is not None:
        # Get filtered notifications (read/unread)
        if is_read:
            notifications = db.query(Notification).filter(
                Notification.recipient_id == user_id,
                Notification.is_read == True
            ).offset(skip).limit(limit).all()
        else:
            notifications = notification_service.get_multi_unread_by_recipient(db, user_id, skip, limit)
    else:
        # Get all notifications for user
        notifications = notification_service.get_multi_by_recipient(db, user_id, skip, limit)

    return notifications


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get current user ID
    user_id = current_user["user"].id

    notification = notification_service.get(db, notification_id, user_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.post("/", response_model=NotificationResponse)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get current user ID (sender)
    sender_id = current_user["user"].id
    hospital_id = current_user["user"].hospital_id

    # Verify recipient exists and belongs to same hospital
    recipient = db.query(User).filter(User.id == notification.recipient_id).first()
    if not recipient:
        raise HTTPException(status_code=400, detail="Recipient not found")
    if recipient.hospital_id != hospital_id:
        raise HTTPException(status_code=400, detail="Recipient does not belong to this hospital")

    # Verify related entity belongs to hospital if provided
    # Note: This is a simplified implementation. In a real app, you'd verify based on entity type.
    if notification.related_entity_id and notification.related_entity_type:
        # For now, we'll just accept that the validation happens at the service level if needed
        pass

    # Prepare notification data
    notification_data = notification.dict()

    return notification_service.create(db, obj_in=notification_data)


@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(
    notification_id: int,
    notification: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get current user ID
    user_id = current_user["user"].id

    # Get existing notification and verify it belongs to the user
    db_notification = notification_service.get(db, notification_id, user_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")

    # Update notification
    return notification_service.update(db, db_obj=db_notification, obj_in=notification)


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get current user ID
    user_id = current_user["user"].id

    # Get existing notification and verify it belongs to the user
    db_notification = notification_service.get(db, notification_id, user_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")

    # Delete notification
    notification_service.remove(db, id=notification_id)
    return {"message": "Notification deleted successfully"}