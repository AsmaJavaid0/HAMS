from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Asset, Department, Location, User
from app.schemas import AssetCreate, AssetUpdate, AssetResponse
from app.dependencies import get_current_user
from app.services.asset import AssetService

router = APIRouter(
    prefix="/api/assets",
    tags=["Assets"],
)

asset_service = AssetService()


@router.get("/", response_model=List[AssetResponse])
def get_assets(
    skip: int = 0,
    limit: int = 100,
    department_id: Optional[int] = None,
    location_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id
    user_role = current_user["role"]

    # Check authorization: all roles can view assets (with hospital isolation)
    if user_role not in ["admin", "nurse", "biomedical"]:
        raise HTTPException(status_code=403, detail="Not authorized to access assets")

    if department_id:
        # Verify department belongs to hospital
        department = db.query(Department).filter(
            Department.id == department_id,
            Department.hospital_id == hospital_id
        ).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        assets = asset_service.get_by_hospital_and_department(db, hospital_id, department_id, skip, limit)
    elif location_id:
        # Verify location belongs to hospital
        location = db.query(Location).filter(
            Location.id == location_id,
            Location.hospital_id == hospital_id
        ).first()
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        assets = asset_service.get_by_hospital_and_location(db, hospital_id, location_id, skip, limit)
    else:
        assets = asset_service.get_by_hospital(db, hospital_id, skip, limit)

    # Apply status filter if provided (service methods don't include status filter yet)
    if status:
        assets = [asset for asset in assets if asset.operational_status == status]

    return assets


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id
    user_role = current_user["role"]

    # Check authorization: all roles can view assets (with hospital isolation)
    if user_role not in ["admin", "nurse", "biomedical"]:
        raise HTTPException(status_code=403, detail="Not authorized to access assets")

    # We'll get by integer id and then check hospital.
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    if db_asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this asset")

    return db_asset


@router.post("/", response_model=AssetResponse)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id
    user_role = current_user["role"]

    # Check authorization: only admin can create assets
    if user_role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create assets")

    # Verify department belongs to hospital if provided
    if asset.department_id:
        department = db.query(Department).filter(
            Department.id == asset.department_id,
            Department.hospital_id == hospital_id
        ).first()
        if not department:
            raise HTTPException(status_code=400, detail="Department does not belong to this hospital")

    # Verify location belongs to hospital if provided
    if asset.location_id:
        location = db.query(Location).filter(
            Location.id == asset.location_id,
            Location.hospital_id == hospital_id
        ).first()
        if not location:
            raise HTTPException(status_code=400, detail="Location does not belong to this hospital")

    # Check if asset_id already exists in this hospital
    existing_asset = asset_service.get_by_asset_id(asset.asset_id, hospital_id)
    if existing_asset:
        raise HTTPException(status_code=409, detail="Asset ID already exists")

    # Prepare asset data with hospital_id
    asset_data = asset.dict()
    asset_data["hospital_id"] = hospital_id

    return asset_service.create(db, obj_in=asset_data)


@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int,
    asset: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id
    user_role = current_user["role"]

    # Check authorization: only admin can update assets
    if user_role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update assets")

    # Get existing asset and verify it belongs to the hospital
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    if db_asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this asset")

    update_data = asset.dict(exclude_unset=True)

    # Verify department belongs to hospital if being updated
    if "department_id" in update_data and update_data["department_id"]:
        department = db.query(Department).filter(
            Department.id == update_data["department_id"],
            Department.hospital_id == hospital_id
        ).first()
        if not department:
            raise HTTPException(status_code=400, detail="Department does not belong to this hospital")

    # Verify location belongs to hospital if being updated
    if "location_id" in update_data and update_data["location_id"]:
        location = db.query(Location).filter(
            Location.id == update_data["location_id"],
            Location.hospital_id == hospital_id
        ).first()
        if not location:
            raise HTTPException(status_code=400, detail="Location does not belong to this hospital")

    # Check if asset_id is being updated and already exists in this hospital (excluding current asset)
    if "asset_id" in update_data and update_data["asset_id"]:
        existing_asset = asset_service.get_by_asset_id(update_data["asset_id"], hospital_id)
        if existing_asset and existing_asset.id != asset_id:
            raise HTTPException(status_code=409, detail="Asset ID already exists")

    # Update asset
    return asset_service.update(db, db_obj=db_asset, obj_in=update_data)


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id
    user_role = current_user["role"]

    # Check authorization: only admin can delete assets
    if user_role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete assets")

    # Get existing asset and verify it belongs to the hospital
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    if db_asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this asset")

    # Delete asset
    asset_service.remove(db, id=asset_id)
    return {"message": "Asset deleted successfully"}