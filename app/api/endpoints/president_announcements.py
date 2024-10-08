# app/api/endpoints/documents.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas import schemas
from app.crud.crud_president_announcement import crud_president_announcement
from app.api import deps
from app.utils import utils

router = APIRouter()


@router.post("/", response_model=schemas.PresidentAnnouncement)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    file_path = "app/static/president_announcements"
    saved_path = utils.save_upload_file(file, file_path)
    document = crud_president_announcement.create_document(
        db=db, file_path=saved_path, user_id=current_user.id
    )
    return document


@router.get("/all", response_model=list[schemas.PresidentAnnouncement])
def read_documents(skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)):
    documents = crud_president_announcement.get_documents(db, skip=skip, limit=limit)
    return documents


@router.get("/{document_id}", response_model=schemas.DocumentWithFile)
def read_document(document_id: int, db: Session = Depends(deps.get_db)):
    document = crud_president_announcement.get_document_by_id(
        db, document_id=document_id
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    file_path = document.file_path
    with open(file_path, "rb") as file:
        file_content = file.read()

    return schemas.DocumentWithFile(
        id=document.id,
        file_path=document.file_path,
        uploaded_at=document.uploaded_at,
        file=file_content,
    )


@router.put("/{document_id}", response_model=schemas.PresidentAnnouncement)
async def update_document(
    document_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document = crud_president_announcement.get_document_by_id(
        db, document_id=document_id
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this document"
        )

    file_path = "app/static/president_announcements"
    saved_path = utils.save_upload_file(file, file_path)
    updated_document = crud_president_announcement.update_document(
        db=db, document_id=document_id, new_file_path=saved_path
    )
    return updated_document


@router.delete("/{document_id}", response_model=schemas.PresidentAnnouncement)
def delete_document(
    document_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document = crud_president_announcement.get_document_by_id(
        db, document_id=document_id
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this document"
        )
    return crud_president_announcement.delete_document(db, document_id=document_id)
