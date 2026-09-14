from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Asset, Department, Location, User
from app.schemas import AssetCreate, AssetUpdate, AssetResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/assets",
    tags=["Assets"],
)


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
    query = db.query(Asset)

    # Filter by hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if hospital_id:
        query = query.filter(Asset.hospital_id == hospital_id)

    # Additional filters
    if department_id:
        query = query.filter(Asset.department_id == department_id)
    if location_id:
        query = query.filter(Asset.location_id == location_id)
    if status:
        query = query.filter(Asset.operational_status == status)

    assets = query.offset(skip).limit(limit).all()
    return assets


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Verify asset belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this asset")

    return asset


@router.post("/", response_model=AssetResponse)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verify hospital exists
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if not hospital_id:
        raise HTTPException(status_code=400, detail="User not associated with a hospital")

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

    # Check if asset_id already exists
    existing_asset = db.query(Asset).filter(Asset.asset_id == asset.asset_id).first()
    if existing_asset:
        raise HTTPException(status_code=409, detail="Asset ID already exists")

    db_asset = Asset(**asset.dict(), hospital_id=hospital_id)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int,
    asset: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Verify asset belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
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

    # Check if asset_id is being updated and already exists
    if "asset_id" in update_data and update_data["asset_id"]:
        existing_asset = db.query(Asset).filter(
            Asset.asset_id == update_data["asset_id"],
            Asset.id != asset_id
        ).first()
        if existing_asset:
            raise HTTPException(status_code=409, detail="Asset ID already exists")

    for key, value in update_data.items():
        setattr(db_asset, key, value)

    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Verify asset belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if db_asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this asset")

    db.delete(db_asset)
    db.commit()
    return {"message": "Asset deleted successfully"}