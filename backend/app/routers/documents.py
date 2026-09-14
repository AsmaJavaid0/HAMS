from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import AssetDocument, Asset, User
from app.schemas import AssetDocumentCreate, AssetDocumentResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)


@router.get("/", response_model=List[AssetDocumentResponse])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = db.query(AssetDocument)

    # Filter by hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if hospital_id:
        query = query.join(Asset).filter(Asset.hospital_id == hospital_id)

    if asset_id:
        query = query.filter(AssetDocument.asset_id == asset_id)

    documents = query.offset(skip).limit(limit).all()
    return documents


@router.get("/{document_id}", response_model=AssetDocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    document = db.query(AssetDocument).filter(AssetDocument.id == document_id).first()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    # Verify document belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    asset = db.query(Asset).filter(Asset.id == document.asset_id).first()
    if not asset or asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this document")

    return document


@router.post("/", response_model=AssetDocumentResponse)
def create_document(
    document: AssetDocumentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verify hospital exists
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    if not hospital_id:
        raise HTTPException(status_code=400, detail="User not associated with a hospital")

    # Verify asset belongs to hospital
    asset = db.query(Asset).filter(
        Asset.id == document.asset_id,
        Asset.hospital_id == hospital_id
    ).first()
    if not asset:
        raise HTTPException(status_code=400, detail="Asset does not belong to this hospital")

    # Verify uploaded_by user exists and belongs to hospital
    uploader = db.query(User).filter(User.id == document.uploaded_by).first()
    if not uploader or uploader.hospital_id != hospital_id:
        raise HTTPException(status_code=400, detail="Uploader does not belong to this hospital")

    db_document = AssetDocument(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_document = db.query(AssetDocument).filter(AssetDocument.id == document_id).first()
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    # Verify document belongs to user's hospital
    hospital_id = db.query(User.hospital_id).filter(User.id == current_user["user"].id).scalar()
    asset = db.query(Asset).filter(Asset.id == db_document.asset_id).first()
    if not asset or asset.hospital_id != hospital_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this document")

    db.delete(db_document)
    db.commit()
    return {"message": "Document deleted successfully"}