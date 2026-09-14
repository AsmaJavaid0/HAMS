from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import AuditLog, User
from app.schemas import AuditLogCreate, AuditLogUpdate, AuditLogResponse
from app.dependencies import get_current_user
from app.services.audit import AuditLogService

router = APIRouter(
    prefix="/api/audit",
    tags=["Audit"],
)

audit_service = AuditLogService()


@router.get("/", response_model=List[AuditLogResponse])
def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    if entity_type and entity_id:
        # Get audit logs for specific entity (with hospital verification)
        audit_logs = audit_service.get_multi_by_entity(db, hospital_id, entity_type, entity_id, skip, limit)
    else:
        # Get all audit logs for hospital
        audit_logs = audit_service.get_multi(db, hospital_id, skip, limit)

    return audit_logs


@router.get("/{audit_id}", response_model=AuditLogResponse)
def get_audit_log(
    audit_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    audit_log = audit_service.get(db, audit_id, hospital_id)
    if audit_log is None:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return audit_log


@router.post("/", response_model=AuditLogResponse)
def create_audit_log(
    audit_log: AuditLogCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Verify user exists and belongs to same hospital if user_id is provided
    if audit_log.user_id:
        user = db.query(User).filter(User.id == audit_log.user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        if user.hospital_id != hospital_id:
            raise HTTPException(status_code=400, detail="User does not belong to this hospital")

    # Verify asset belongs to hospital if entity_type is asset
    if audit_log.entity_type and audit_log.entity_type.lower() == "asset" and audit_log.entity_id:
        asset = db.query(Asset).filter(
            Asset.id == audit_log.entity_id,
            Asset.hospital_id == hospital_id
        ).first()
        if not asset:
            raise HTTPException(status_code=400, detail="Asset does not belong to this hospital")

    # Prepare audit log data
    audit_log_data = audit_log.dict()

    return audit_service.create(db, obj_in=audit_log_data)


@router.put("/{audit_id}", response_model=AuditLogResponse)
def update_audit_log(
    audit_id: int,
    audit_log: AuditLogUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing audit log and verify it belongs to the hospital
    db_audit_log = audit_service.get(db, audit_id, hospital_id)
    if db_audit_log is None:
        raise HTTPException(status_code=404, detail="Audit log not found")

    # Update audit log
    return audit_service.update(db, db_obj=db_audit_log, obj_in=audit_log)


@router.delete("/{audit_id}")
def delete_audit_log(
    audit_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing audit log and verify it belongs to the hospital
    db_audit_log = audit_service.get(db, audit_id, hospital_id)
    if db_audit_log is None:
        raise HTTPException(status_code=404, detail="Audit log not found")

    # Delete audit log
    audit_service.remove(db, id=audit_id)
    return {"message": "Audit log deleted successfully"}