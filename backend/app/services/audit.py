from app.services.base import BaseService
from app.models import AuditLog, Asset
from app.schemas import AuditLogCreate, AuditLogUpdate
from sqlalchemy.orm import Session
from typing import List, Optional


class AuditLogService(BaseService[AuditLog, AuditLogCreate, AuditLogUpdate]):
    def __init__(self):
        super().__init__(AuditLog)

    def get(self, db: Session, id: int, hospital_id: int):
        return db.query(AuditLog).join(AuditLog.asset).filter(
            AuditLog.id == id,
            Asset.hospital_id == hospital_id
        ).first()

    def get_multi(self, db: Session, hospital_id: int, skip: int = 0, limit: int = 100):
        return db.query(AuditLog).join(AuditLog.asset).filter(
            Asset.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    def get_multi_by_entity(self, db: Session, hospital_id: int, entity_type: str, entity_id: int, skip: int = 0, limit: int = 100):
        return db.query(AuditLog).join(AuditLog.asset).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id,
            Asset.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()