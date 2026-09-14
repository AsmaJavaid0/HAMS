from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import AssetMovement, Asset, Department, Location, User
from app.schemas import AssetMovementCreate, AssetMovementResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/movements",
    tags=["Movements"],
)


@router.get("/", response_model=List[AssetMovementResponse])
def get_movements(
    skip: int = 0,
    limit: int = 100,
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = db.query(AssetMovement)

    # Filter by hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if hospital_id:
        query = query.join(Asset).filter(Asset.hospital_id == hospital_id)

    if asset_id:
        query = query.filter(AssetMovement.asset_id == asset_id)

    movements = query.offset(skip).limit(limit).all()
    return movements


@router.get("/{movement_id}", response_model=AssetMovementResponse)
def get_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    movement = db.query(AssetMovement).filter(AssetMovement.id == movement_id).first()
    if movement is None:
        raise HTTPException(status_code=404, detail="Movement not found")

    # Verify movement belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    asset = db.query(Asset).filter(Asset.id == movement.asset_id).first()
    if not asset or asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this movement")

    return movement


@router.post("/", response_model=AssetMovementResponse)
def create_movement(
    movement: AssetMovementCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verify hospital exists
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if not hospital_id:
        raise HTTPException(status_code=400, detail="User not associated with a hospital")

    # Verify asset belongs to hospital
    asset = db.query(Asset).filter(
        Asset.id == movement.asset_id,
        Asset.hospital_id == hospital_id
    ).first()
    if not asset:
        raise HTTPException(status_code=400, detail="Asset does not belong to this hospital")

    # Verify from_department belongs to hospital if provided
    if movement.from_department_id:
        from_dept = db.query(Department).filter(
            Department.id == movement.from_department_id,
            Department.hospital_id == hospital_id
        ).first()
        if not from_dept:
            raise HTTPException(status_code=400, detail="From department does not belong to this hospital")

    # Verify to_department belongs to hospital if provided
    if movement.to_department_id:
        to_dept = db.query(Department).filter(
            Department.id == movement.to_department_id,
            Department.hospital_id == hospital_id
        ).first()
        if not to_dept:
            raise HTTPException(status_code=400, detail="To department does not belong to this hospital")

    # Verify from_location belongs to hospital if provided
    if movement.from_location_id:
        from_loc = db.query(Location).filter(
            Location.id == movement.from_location_id,
            Location.hospital_id == hospital_id
        ).first()
        if not from_loc:
            raise HTTPException(status_code=400, detail="From location does not belong to this hospital")

    # Verify to_location belongs to hospital if provided
    if movement.to_location_id:
        to_loc = db.query(Location).filter(
            Location.id == movement.to_location_id,
            Location.hospital_id == hospital_id
        ).first()
        if not to_loc:
            raise HTTPException(status_code=400, detail="To location does not belong to this hospital")

    # Verify mover exists and belongs to hospital
    mover = db.query(User).filter(User.id == movement.moved_by).first()
    if not mover or mover.hospital_id != hospital_id:
        raise HTTPException(status_code=400, detail="Mover does not belong to this hospital")

    db_movement = AssetMovement(**movement.dict())
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement


@router.delete("/{movement_id}")
def delete_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_movement = db.query(AssetMovement).filter(AssetMovement.id == movement_id).first()
    if db_movement is None:
        raise HTTPException(status_code=404, detail="Movement not found")

    # Verify movement belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    asset = db.query(Asset).filter(Asset.id == db_movement.asset_id).first()
    if not asset or asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this movement")

    db.delete(db_movement)
    db.commit()
    return {"message": "Movement deleted successfully"}