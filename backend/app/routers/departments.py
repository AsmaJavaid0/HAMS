from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Department, User
from app.schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.dependencies import get_current_user
from app.services.department import DepartmentService

router = APIRouter(
    prefix="/api/departments",
    tags=["Departments"],
)

department_service = DepartmentService()


@router.get("/", response_model=List[DepartmentResponse])
def get_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id
    user_role = current_user["role"]

    # Check authorization: admin and biomedical can view departments
    if user_role not in ["admin", "biomedical"]:
        raise HTTPException(status_code=403, detail="Not authorized to view departments")

    departments = department_service.get_by_hospital(db, hospital_id, skip, limit)
    return departments


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id
    department = db.query(Department).filter(
        Department.id == department_id,
        Department.hospital_id == hospital_id
    ).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.post("/", response_model=DepartmentResponse)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Check if department code already exists in this hospital
    existing = department_service.get_by_code(db, department.code, hospital_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department with this code already exists"
        )

    # Create department with hospital_id
    department_data = department.dict()
    department_data["hospital_id"] = hospital_id
    return department_service.create(db, obj_in=department_data)


@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing department and verify it belongs to the hospital
    db_department = db.query(Department).filter(
        Department.id == department_id,
        Department.hospital_id == hospital_id
    ).first()
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    # Check if updating to a code that already exists in this hospital (excluding current department)
    if department.code and department.code != db_department.code:
        existing = department_service.get_by_code(db, department.code, hospital_id)
        if existing and existing.id != department_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Department with this code already exists"
            )

    # Update department
    return department_service.update(db, db_obj=db_department, obj_in=department)


@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing department and verify it belongs to the hospital
    db_department = db.query(Department).filter(
        Department.id == department_id,
        Department.hospital_id == hospital_id
    ).first()
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    # Check if department has assets
    asset_count = db.query(Department).filter(Department.id == department_id).join(
        Department.assets
    ).count()
    if asset_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete department that has assets assigned to it"
        )

    # Delete department
    department_service.remove(db, id=department_id)
    return {"message": "Department deleted successfully"}