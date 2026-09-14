from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import AuditLog, User
from app.schemas import AuditLogCreate, AuditLogResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/audit",
    tags=["Audit"],
)


@router.get("/", response_model=List[AuditLogResponse])
def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = db.query(AuditLog)

    # Filter by hospital - only show logs for assets in user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if hospital_id:
        query = query.join(AuditLog.asset).filter(AuditLog.asset.has(hospital_id=hospital_id))

    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    if entity_id:
        query = query.filter(AuditLog.entity_id == entity_id)

    audit_logs = query.offset(skip).limit(limit).all()
    return audit_logs


@router.get("/{audit_id}", response_model=AuditLogResponse)
def get_audit_log(
    audit_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    audit_log = db.query(AuditLog).filter(AuditLog.id == audit_id).first()
    if audit_log is None:
        raise HTTPException(status_code=404, detail="Audit log not found")

    # Verify audit log belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if not audit_log.asset or audit_log.asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this audit log")

    return audit_log


@router.post("/", response_model=AuditLogResponse)
def create_audit_log(
    audit_log: AuditLogCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verify user exists and belongs to same hospital if user_id is provided
    if audit_log.user_id:
        user = db.query(User).filter(User.id == audit_log.user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
        if user.hospital_id != hospital_id:
            raise HTTPException(status_code=400, detail="User does not belong to this hospital")

    # Verify asset belongs to hospital if entity_type is asset
    if audit_log.entity_type.lower() == "asset" and audit_log.entity_id:
        asset = db.query(User.hospital_id).join(
            Asset, Asset.hospital_id == User.hospital_id
        ).filter(
            Asset.id == audit_log.entity_id,
            User.id == current_user["user"].id
        ).first()
        if not asset:
            raise HTTPException(status_code=400, detail="Asset does not belong to this hospital")

    db_audit_log = AuditLog(**audit_log.dict())
    db.add(db_audit_log)
    db.commit()
    db.refresh(db_audit_log)
    return db_audit_log