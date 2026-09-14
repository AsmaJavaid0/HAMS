from app.services.base import BaseService
from app.models import AssetDocument, Asset
from app.schemas import AssetDocumentCreate, AssetDocumentUpdate
from sqlalchemy.orm import Session
from typing import List, Optional


class AssetDocumentService(BaseService[AssetDocument, AssetDocumentCreate, AssetDocumentUpdate]):
    def __init__(self):
        super().__init__(AssetDocument)

    def get(self, db: Session, id: int, hospital_id: int):
        return db.query(AssetDocument).join(AssetDocument.asset).filter(
            AssetDocument.id == id,
            Asset.hospital_id == hospital_id
        ).first()

    def get_multi(self, db: Session, hospital_id: int, skip: int = 0, limit: int = 100):
        return db.query(AssetDocument).join(AssetDocument.asset).filter(
            Asset.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    def get_multi_by_asset(self, db: Session, hospital_id: int, asset_id: int, skip: int = 0, limit: int = 100):
        return db.query(AssetDocument).join(AssetDocument.asset).filter(
            AssetDocument.asset_id == asset_id,
            Asset.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()