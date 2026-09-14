from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Department, User
from app.schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/departments",
    tags=["Departments"],
)


@router.get("/", response_model=List[DepartmentResponse])
def get_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    departments = db.query(Department).offset(skip).limit(limit).all()
    return departments


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.post("/", response_model=DepartmentResponse)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verify hospital exists
    hospital = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if not hospital:
        raise HTTPException(status_code=400, detail="User not associated with a hospital")

    db_department = Department(**department.dict(), hospital_id=hospital)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    update_data = department.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_department, key, value)

    db.commit()
    db.refresh(db_department)
    return db_department


@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    db.delete(db_department)
    db.commit()
    return {"message": "Department deleted successfully"}