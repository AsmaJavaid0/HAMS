from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Location, Department, User
from app.schemas import LocationCreate, LocationUpdate, LocationResponse
from app.dependencies import get_current_user
from app.services.location import LocationService

router = APIRouter(
    prefix="/api/locations",
    tags=["Locations"],
)

location_service = LocationService()


@router.get("/", response_model=List[LocationResponse])
def get_locations(
    skip: int = 0,
    limit: int = 100,
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    if department_id:
        # Verify department belongs to hospital
        department = db.query(Department).filter(
            Department.id == department_id,
            Department.hospital_id == hospital_id
        ).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        locations = location_service.get_by_hospital_and_department(db, hospital_id, department_id, skip, limit)
    else:
        locations = location_service.get_by_hospital(db, hospital_id, skip, limit)

    return locations


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    location = db.query(Location).filter(
        Location.id == location_id,
        Location.hospital_id == hospital_id
    ).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.post("/", response_model=LocationResponse)
def create_location(
    location: LocationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # If department_id is provided, verify it belongs to the same hospital
    if location.department_id:
        dept = db.query(Department).filter(
            Department.id == location.department_id,
            Department.hospital_id == hospital_id
        ).first()
        if not dept:
            raise HTTPException(status_code=400, detail="Department does not belong to this hospital")

    # Prepare location data with hospital_id
    location_data = location.dict()
    location_data["hospital_id"] = hospital_id

    return location_service.create(db, obj_in=location_data)


@router.put("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int,
    location: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing location and verify it belongs to the hospital
    db_location = db.query(Location).filter(
        Location.id == location_id,
        Location.hospital_id == hospital_id
    ).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    # If department_id is being updated, verify it belongs to the same hospital
    if location.department_id and location.department_id != db_location.department_id:
        dept = db.query(Department).filter(
            Department.id == location.department_id,
            Department.hospital_id == hospital_id
        ).first()
        if not dept:
            raise HTTPException(status_code=400, detail="Department does not belong to this hospital")

    # Update location
    return location_service.update(db, db_obj=db_location, obj_in=location)


@router.delete("/{location_id}")
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing location and verify it belongs to the hospital
    db_location = db.query(Location).filter(
        Location.id == location_id,
        Location.hospital_id == hospital_id
    ).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    # Check if location has child locations
    child_count = db.query(Location).filter(Location.parent_id == location_id).count()
    if child_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete location that has child locations"
        )

    # Check if location has assets
    asset_count = db.query(Location).filter(Location.id == location_id).join(
        Location.assets
    ).count()
    if asset_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete location that has assets assigned to it"
        )

    # Delete location
    location_service.remove(db, id=location_id)
    return {"message": "Location deleted successfully"}


@router.get("/{location_id}/children", response_model=List[LocationResponse])
def get_location_children(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Verify parent location exists and belongs to hospital
    parent_location = db.query(Location).filter(
        Location.id == location_id,
        Location.hospital_id == hospital_id
    ).first()
    if parent_location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    # Get children
    children = location_service.get_children(db, location_id, hospital_id)
    return children


@router.get("/root", response_model=List[LocationResponse])
def get_root_locations(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get root locations (those without parent)
    roots = location_service.get_root_locations(db, hospital_id)
    return roots