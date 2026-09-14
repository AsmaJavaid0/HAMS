from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Compliance, Asset, User
from app.schemas import ComplianceCreate, ComplianceUpdate, ComplianceResponse
from app.dependencies import get_current_user
from app.services.compliance import ComplianceService

router = APIRouter(
    prefix="/api/compliance",
    tags=["Compliance"],
)

compliance_service = ComplianceService()


@router.get("/", response_model=List[ComplianceResponse])
def get_compliance_records(
    skip: int = 0,
    limit: int = 100,
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    if asset_id:
        # Get compliance records for specific asset (with hospital verification)
        compliance_records = compliance_service.get_multi_by_asset(db, hospital_id, asset_id, skip, limit)
    else:
        # Get all compliance records for hospital
        compliance_records = compliance_service.get_multi(db, hospital_id, skip, limit)

    return compliance_records


@router.get("/{compliance_id}", response_model=ComplianceResponse)
def get_compliance_record(
    compliance_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    compliance = compliance_service.get(db, compliance_id, hospital_id)
    if compliance is None:
        raise HTTPException(status_code=404, detail="Compliance record not found")
    return compliance


@router.post("/", response_model=ComplianceResponse)
def create_compliance_record(
    compliance: ComplianceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Verify asset belongs to hospital
    asset = db.query(Asset).filter(
        Asset.id == compliance.asset_id,
        Asset.hospital_id == hospital_id
    ).first()
    if not asset:
        raise HTTPException(status_code=400, detail="Asset does not belong to this hospital")

    # Prepare compliance data
    compliance_data = compliance.dict()

    return compliance_service.create(db, obj_in=compliance_data)


@router.put("/{compliance_id}", response_model=ComplianceResponse)
def update_compliance_record(
    compliance_id: int,
    compliance: ComplianceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing compliance and verify it belongs to the hospital
    db_compliance = compliance_service.get(db, compliance_id, hospital_id)
    if db_compliance is None:
        raise HTTPException(status_code=404, detail="Compliance record not found")

    # Update compliance
    return compliance_service.update(db, db_obj=db_compliance, obj_in=compliance)


@router.delete("/{compliance_id}")
def delete_compliance_record(
    compliance_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing compliance and verify it belongs to the hospital
    db_compliance = compliance_service.get(db, compliance_id, hospital_id)
    if db_compliance is None:
        raise HTTPException(status_code=404, detail="Compliance record not found")

    # Delete compliance
    compliance_service.remove(db, id=compliance_id)
    return {"message": "Compliance record deleted successfully"}