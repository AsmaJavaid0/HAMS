from app.services.base import BaseService
from app.models import Asset
from app.schemas import AssetCreate, AssetUpdate

class AssetService(BaseService[Asset, AssetCreate, AssetUpdate]):
    def __init__(self):
        super().__init__(Asset)

    def get_by_hospital(self, db, hospital_id: int, skip: int = 0, limit: int = 100):
        return db.query(Asset).filter(
            Asset.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    def get_by_hospital_and_department(self, db, hospital_id: int, department_id: int, skip: int = 0, limit: int = 100):
        return db.query(Asset).filter(
            Asset.hospital_id == hospital_id,
            Asset.department_id == department_id
        ).offset(skip).limit(limit).all()

    def get_by_hospital_and_location(self, db, hospital_id: int, location_id: int, skip: int = 0, limit: int = 100):
        return db.query(Asset).filter(
            Asset.hospital_id == hospital_id,
            Asset.location_id == location_id
        ).offset(skip).limit(limit).all()

    def get_by_asset_id(self, db, asset_id: str, hospital_id: int):
        return db.query(Asset).filter(
            Asset.asset_id == asset_id,
            Asset.hospital_id == hospital_id
        ).first()