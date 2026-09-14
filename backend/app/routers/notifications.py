from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Notification, User
from app.schemas import NotificationCreate, NotificationUpdate, NotificationResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"],
)


@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    skip: int = 0,
    limit: int = 100,
    is_read: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = db.query(Notification).filter(Notification.recipient_id == current_user["user"].id)

    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)

    notifications = query.offset(skip).limit(limit).all()
    return notifications


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.recipient_id == current_user["user"].id
    ).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.post("/", response_model=NotificationResponse)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verify recipient exists and belongs to same hospital
    recipient = db.query(User).filter(User.id == notification.recipient_id).first()
    if not recipient:
        raise HTTPException(status_code=400, detail="Recipient not found")

    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if recipient.hospital_id != hospital_id:
        raise HTTPException(status_code=400, detail="Recipient does not belong to this hospital")

    # Verify related entity belongs to hospital if provided
    if notification.related_entity_id and notification.related_entity_type:
        # This is a simplified check - in a real app you'd verify the entity type and ID
        pass

    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(
    notification_id: int,
    notification: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.recipient_id == current_user["user"].id
    ).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")

    update_data = notification.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_notification, key, value)

    db.commit()
    db.refresh(db_notification)
    return db_notification


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.recipient_id == current_user["user"].id
    ).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(db_notification)
    db.commit()
    return {"message": "Notification deleted successfully"}