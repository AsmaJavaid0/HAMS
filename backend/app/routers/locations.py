from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Location, Department, User
from app.schemas import LocationCreate, LocationUpdate, LocationResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/locations",
    tags=["Locations"],
)


@router.get("/", response_model=List[LocationResponse])
def get_locations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    locations = db.query(Location).offset(skip).limit(limit).all()
    return locations


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.post("/", response_model=LocationResponse)
def create_location(
    location: LocationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verify hospital exists
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if not hospital_id:
        raise HTTPException(status_code=400, detail="User not associated with a hospital")

    # If department_id is provided, verify it belongs to the same hospital
    if location.department_id:
        dept = db.query(Department).filter(
            Department.id == location.department_id,
            Department.hospital_id == hospital_id
        ).first()
        if not dept:
            raise HTTPException(status_code=400, detail="Department does not belong to this hospital")

    db_location = Location(**location.dict(), hospital_id=hospital_id)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


@router.put("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int,
    location: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    update_data = location.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_location, key, value)

    db.commit()
    db.refresh(db_location)
    return db_location


@router.delete("/{location_id}")
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    db.delete(db_location)
    db.commit()
    return {"message": "Location deleted successfully"}