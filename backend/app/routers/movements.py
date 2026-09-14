from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import AssetMovement, Asset, Department, Location, User
from app.schemas import AssetMovementCreate, AssetMovementUpdate, AssetMovementResponse
from app.dependencies import get_current_user
from app.services.movement import AssetMovementService

router = APIRouter(
    prefix="/api/movements",
    tags=["Movements"],
)

movement_service = AssetMovementService()


@router.get("/", response_model=List[AssetMovementResponse])
def get_movements(
    skip: int = 0,
    limit: int = 100,
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    if asset_id:
        # Get movements for specific asset (with hospital verification)
        movements = movement_service.get_multi_by_asset(db, hospital_id, asset_id, skip, limit)
    else:
        # Get all movements for hospital
        movements = movement_service.get_multi(db, hospital_id, skip, limit)

    return movements


@router.get("/{movement_id}", response_model=AssetMovementResponse)
def get_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    movement = movement_service.get(db, movement_id, hospital_id)
    if movement is None:
        raise HTTPException(status_code=404, detail="Movement not found")
    return movement


@router.post("/", response_model=AssetMovementResponse)
def create_movement(
    movement: AssetMovementCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

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

    # Prepare movement data
    movement_data = movement.dict()

    return movement_service.create(db, obj_in=movement_data)


@router.put("/{movement_id}", response_model=AssetMovementResponse)
def update_movement(
    movement_id: int,
    movement: AssetMovementUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing movement and verify it belongs to the hospital
    db_movement = movement_service.get(db, movement_id, hospital_id)
    if db_movement is None:
        raise HTTPException(status_code=404, detail="Movement not found")

    # Update movement
    return movement_service.update(db, db_obj=db_movement, obj_in=movement)


@router.delete("/{movement_id}")
def delete_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing movement and verify it belongs to the hospital
    db_movement = movement_service.get(db, movement_id, hospital_id)
    if db_movement is None:
        raise HTTPException(status_code=404, detail="Movement not found")

    # Delete movement
    movement_service.remove(db, id=movement_id)
    return {"message": "Movement deleted successfully"}