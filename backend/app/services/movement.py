from app.services.base import BaseService
from app.models import AssetMovement, Asset
from app.schemas import AssetMovementCreate, AssetMovementUpdate
from sqlalchemy.orm import Session
from typing import List, Optional


class AssetMovementService(BaseService[AssetMovement, AssetMovementCreate, AssetMovementUpdate]):
    def __init__(self):
        super().__init__(AssetMovement)

    def get(self, db: Session, id: int, hospital_id: int):
        return db.query(AssetMovement).join(AssetMovement.asset).filter(
            AssetMovement.id == id,
            Asset.hospital_id == hospital_id
        ).first()

    def get_multi(self, db: Session, hospital_id: int, skip: int = 0, limit: int = 100):
        return db.query(AssetMovement).join(AssetMovement.asset).filter(
            Asset.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    def get_multi_by_asset(self, db: Session, hospital_id: int, asset_id: int, skip: int = 0, limit: int = 100):
        return db.query(AssetMovement).join(AssetMovement.asset).filter(
            AssetMovement.asset_id == asset_id,
            Asset.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()