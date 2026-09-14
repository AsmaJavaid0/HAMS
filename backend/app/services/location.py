from app.services.base import BaseService
from app.models import Location
from app.schemas import LocationCreate, LocationUpdate

class LocationService(BaseService[Location, LocationCreate, LocationUpdate]):
    def __init__(self):
        super().__init__(Location)

    def get_by_hospital(self, db, hospital_id: int, skip: int = 0, limit: int = 100):
        return db.query(Location).filter(
            Location.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    def get_by_hospital_and_department(self, db, hospital_id: int, department_id: int, skip: int = 0, limit: int = 100):
        return db.query(Location).filter(
            Location.hospital_id == hospital_id,
            Location.department_id == department_id
        ).offset(skip).limit(limit).all()

    def get_root_locations(self, db, hospital_id: int, skip: int = 0, limit: int = 100):
        return db.query(Location).filter(
            Location.hospital_id == hospital_id,
            Location.parent_id.is_(None)
        ).offset(skip).limit(limit).all()

    def get_children(self, db, parent_id: int, hospital_id: int, skip: int = 0, limit: int = 100):
        return db.query(Location).filter(
            Location.parent_id == parent_id,
            Location.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()