from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Maintenance, Asset, User
from app.schemas import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/maintenance",
    tags=["Maintenance"],
)


@router.get("/", response_model=List[MaintenanceResponse])
def get_maintenance_records(
    skip: int = 0,
    limit: int = 100,
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = db.query(Maintenance)

    # Filter by hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if hospital_id:
        query = query.join(Asset).filter(Asset.hospital_id == hospital_id)

    if asset_id:
        query = query.filter(Maintenance.asset_id == asset_id)

    maintenance_records = query.offset(skip).limit(limit).all()
    return maintenance_records


@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance_record(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    # Verify maintenance belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    asset = db.query(Asset).filter(Asset.id == maintenance.asset_id).first()
    if not asset or asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this maintenance record")

    return maintenance


@router.post("/", response_model=MaintenanceResponse)
def create_maintenance_record(
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verify hospital exists
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if not hospital_id:
        raise HTTPException(status_code=400, detail="User not associated with a hospital")

    # Verify asset belongs to hospital
    asset = db.query(Asset).filter(
        Asset.id == maintenance.asset_id,
        Asset.hospital_id == hospital_id
    ).first()
    if not asset:
        raise HTTPException(status_code=400, detail="Asset does not belong to this hospital")

    db_maintenance = Maintenance(**maintenance.dict())
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance


@router.put("/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance_record(
    maintenance_id: int,
    maintenance: MaintenanceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if db_maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    # Verify maintenance belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    asset = db.query(Asset).filter(Asset.id == db_maintenance.asset_id).first()
    if not asset or asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this maintenance record")

    update_data = maintenance.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_maintenance, key, value)

    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance


@router.delete("/{maintenance_id}")
def delete_maintenance_record(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if db_maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    # Verify maintenance belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    asset = db.query(Asset).filter(Asset.id == db_maintenance.asset_id).first()
    if not asset or asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this maintenance record")

    db.delete(db_maintenance)
    db.commit()
    return {"message": "Maintenance record deleted successfully"}