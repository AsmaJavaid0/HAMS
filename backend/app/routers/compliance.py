from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Compliance, Asset, User
from app.schemas import ComplianceCreate, ComplianceUpdate, ComplianceResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/compliance",
    tags=["Compliance"],
)


@router.get("/", response_model=List[ComplianceResponse])
def get_compliance_records(
    skip: int = 0,
    limit: int = 100,
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = db.query(Compliance)

    # Filter by hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if hospital_id:
        query = query.join(Asset).filter(Asset.hospital_id == hospital_id)

    if asset_id:
        query = query.filter(Compliance.asset_id == asset_id)

    compliance_records = query.offset(skip).limit(limit).all()
    return compliance_records


@router.get("/{compliance_id}", response_model=ComplianceResponse)
def get_compliance_record(
    compliance_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    compliance = db.query(Compliance).filter(Compliance.id == compliance_id).first()
    if compliance is None:
        raise HTTPException(status_code=404, detail="Compliance record not found")

    # Verify compliance belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    asset = db.query(Asset).filter(Asset.id == compliance.asset_id).first()
    if not asset or asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this compliance record")

    return compliance


@router.post("/", response_model=ComplianceResponse)
def create_compliance_record(
    compliance: ComplianceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verify hospital exists
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if not hospital_id:
        raise HTTPException(status_code=400, detail="User not associated with a hospital")

    # Verify asset belongs to hospital
    asset = db.query(Asset).filter(
        Asset.id == compliance.asset_id,
        Asset.hospital_id == hospital_id
    ).first()
    if not asset:
        raise HTTPException(status_code=400, detail="Asset does not belong to this hospital")

    db_compliance = Compliance(**compliance.dict())
    db.add(db_compliance)
    db.commit()
    db.refresh(db_compliance)
    return db_compliance


@router.put("/{compliance_id}", response_model=ComplianceResponse)
def update_compliance_record(
    compliance_id: int,
    compliance: ComplianceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_compliance = db.query(Compliance).filter(Compliance.id == compliance_id).first()
    if db_compliance is None:
        raise HTTPException(status_code=404, detail="Compliance record not found")

    # Verify compliance belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    asset = db.query(Asset).filter(Asset.id == db_compliance.asset_id).first()
    if not asset or asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this compliance record")

    update_data = compliance.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_compliance, key, value)

    db.commit()
    db.refresh(db_compliance)
    return db_compliance


@router.delete("/{compliance_id}")
def delete_compliance_record(
    compliance_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_compliance = db.query(Compliance).filter(Compliance.id == compliance_id).first()
    if db_compliance is None:
        raise HTTPException(status_code=404, detail="Compliance record not found")

    # Verify compliance belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    asset = db.query(Asset).filter(Asset.id == db_compliance.asset_id).first()
    if not asset or asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this compliance record")

    db.delete(db_compliance)
    db.commit()
    return {"message": "Compliance record deleted successfully"}