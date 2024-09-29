# app/api/endpoints/documents.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas import schemas
from app.crud import crud_document
from app.api import deps
from app.utils import utils

router = APIRouter()


@router.post("/", response_model=schemas.KnowledgeDocument)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    file_filename = file.filename
    file_path = f"app/static/documents/{file_filename}"
    utils.save_upload_file(file, file_path)
    document = crud_document.create_document(
        db=db, file_path=file_path, user_id=current_user.id
    )
    return document


@router.get("/", response_model=list[schemas.KnowledgeDocument])
def read_documents(skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)):
    documents = crud_document.get_documents(db, skip=skip, limit=limit)
    return documents


@router.delete("/{document_id}", response_model=schemas.KnowledgeDocument)
def delete_document(
    document_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document = crud_document.__get_document_by_id(db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this document"
        )
    return crud_document.delete_document(db, document_id=document_id)
