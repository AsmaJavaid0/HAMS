from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import AssetDocument, Asset, User
from app.schemas import AssetDocumentCreate, AssetDocumentUpdate, AssetDocumentResponse
from app.dependencies import get_current_user
from app.services.document import AssetDocumentService

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)

document_service = AssetDocumentService()


@router.get("/", response_model=List[AssetDocumentResponse])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    if asset_id:
        # Get documents for specific asset (with hospital verification)
        documents = document_service.get_multi_by_asset(db, hospital_id, asset_id, skip, limit)
    else:
        # Get all documents for hospital
        documents = document_service.get_multi(db, hospital_id, skip, limit)

    return documents


@router.get("/{document_id}", response_model=AssetDocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    document = document_service.get(db, document_id, hospital_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.post("/", response_model=AssetDocumentResponse)
def create_document(
    document: AssetDocumentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Verify asset belongs to hospital
    asset = db.query(Asset).filter(
        Asset.id == document.asset_id,
        Asset.hospital_id == hospital_id
    ).first()
    if not asset:
        raise HTTPException(status_code=400, detail="Asset does not belong to this hospital")

    # Prepare document data
    document_data = document.dict()

    return document_service.create(db, obj_in=document_data)


@router.put("/{document_id}", response_model=AssetDocumentResponse)
def update_document(
    document_id: int,
    document: AssetDocumentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing document and verify it belongs to the hospital
    db_document = document_service.get(db, document_id, hospital_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    # Update document
    return document_service.update(db, db_obj=db_document, obj_in=document)


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Get hospital ID from current user
    hospital_id = current_user["user"].hospital_id

    # Get existing document and verify it belongs to the hospital
    db_document = document_service.get(db, document_id, hospital_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete document
    document_service.remove(db, id=document_id)
    return {"message": "Document deleted successfully"}