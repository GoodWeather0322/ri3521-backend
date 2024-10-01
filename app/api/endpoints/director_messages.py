# app/api/endpoints/documents.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas import schemas
from app.crud.crud_director_message import crud_director_message
from app.api import deps
from app.utils import utils

router = APIRouter()


@router.post("/", response_model=schemas.DirectorMessage)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    file_path = "app/static/director_messages"
    saved_path = utils.save_upload_file(file, file_path)
    document = crud_director_message.create_document(
        db=db, file_path=saved_path, user_id=current_user.id
    )
    return document


@router.get("/all", response_model=list[schemas.DirectorMessage])
def read_documents(skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)):
    documents = crud_director_message.get_documents(db, skip=skip, limit=limit)
    return documents


@router.get("/{document_id}", response_model=schemas.DirectorMessage)
def read_document(document_id: int, db: Session = Depends(deps.get_db)):
    document = crud_director_message.get_document_by_id(db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.put("/{document_id}", response_model=schemas.DirectorMessage)
async def update_document(
    document_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document = crud_director_message.get_document_by_id(db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this document"
        )

    file_path = "app/static/director_messages"
    saved_path = utils.save_upload_file(file, file_path)
    updated_document = crud_director_message.update_document(
        db=db, document_id=document_id, new_file_path=saved_path
    )
    return updated_document


@router.delete("/{document_id}", response_model=schemas.DirectorMessage)
def delete_document(
    document_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document = crud_director_message.get_document_by_id(db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this document"
        )
    return crud_director_message.delete_document(db, document_id=document_id)
