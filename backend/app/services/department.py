from app.services.base import BaseService
from app.models import Department
from app.schemas import DepartmentCreate, DepartmentUpdate

class DepartmentService(BaseService[Department, DepartmentCreate, DepartmentUpdate]):
    def __init__(self):
        super().__init__(Department)

    def get_by_hospital(self, db, hospital_id: int, skip: int = 0, limit: int = 100):
        return db.query(Department).filter(
            Department.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    def get_by_code(self, db, code: str, hospital_id: int):
        return db.query(Department).filter(
            Department.code == code,
            Department.hospital_id == hospital_id
        ).first()