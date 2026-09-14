from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Maintenance, Asset, User
from app.schemas import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse
from app.dependencies import get_current_user
from app.services.maintenance import MaintenanceService

router = APIRouter(
    prefix="/api/maintenance",
    tags=["Maintenance"],
)

maintenance_service = MaintenanceService()


@router.get("/", response_model=List[MaintenanceResponse])
def get_maintenance_records(
    skip: int = 0,
    limit: int = 100,
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    if asset_id:
        # Get maintenance records for specific asset (with hospital verification)
        maintenance_records = maintenance_service.get_multi_by_asset(db, hospital_id, asset_id, skip, limit)
    else:
        # Get all maintenance records for hospital
        maintenance_records = maintenance_service.get_multi(db, hospital_id, skip, limit)

    return maintenance_records


@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance_record(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    maintenance = maintenance_service.get(db, maintenance_id, hospital_id)
    if maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return maintenance


@router.post("/", response_model=MaintenanceResponse)
def create_maintenance_record(
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Verify asset belongs to hospital
    asset = db.query(Asset).filter(
        Asset.id == maintenance.asset_id,
        Asset.hospital_id == hospital_id
    ).first()
    if not asset:
        raise HTTPException(status_code=400, detail="Asset does not belong to this hospital")

    # Prepare maintenance data
    maintenance_data = maintenance.dict()

    return maintenance_service.create(db, obj_in=maintenance_data)


@router.put("/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance_record(
    maintenance_id: int,
    maintenance: MaintenanceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing maintenance and verify it belongs to the hospital
    db_maintenance = maintenance_service.get(db, maintenance_id, hospital_id)
    if db_maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    # Update maintenance
    return maintenance_service.update(db, db_obj=db_maintenance, obj_in=maintenance)


@router.delete("/{maintenance_id}")
def delete_maintenance_record(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing maintenance and verify it belongs to the hospital
    db_maintenance = maintenance_service.get(db, maintenance_id, hospital_id)
    if db_maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    # Delete maintenance
    maintenance_service.remove(db, id=maintenance_id)
    return {"message": "Maintenance record deleted successfully"}