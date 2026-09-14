from app.services.base import BaseService
from app.models import Notification
from app.schemas import NotificationCreate, NotificationUpdate
from sqlalchemy.orm import Session
from typing import List, Optional


class NotificationService(BaseService[Notification, NotificationCreate, NotificationUpdate]):
    def __init__(self):
        super().__init__(Notification)

    def get_multi_by_recipient(self, db: Session, recipient_id: int, skip: int = 0, limit: int = 100):
        return db.query(Notification).filter(
            Notification.recipient_id == recipient_id
        ).offset(skip).limit(limit).all()

    def get_multi_unread_by_recipient(self, db: Session, recipient_id: int, skip: int = 0, limit: int = 100):
        return db.query(Notification).filter(
            Notification.recipient_id == recipient_id,
            Notification.is_read == False
        ).offset(skip).limit(limit).all()

    def get(self, db: Session, id: int, recipient_id: int):
        return db.query(Notification).filter(
            Notification.id == id,
            Notification.recipient_id == recipient_id
        ).first()