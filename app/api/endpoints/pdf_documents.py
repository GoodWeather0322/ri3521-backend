from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session

from app import models
from app.schemas import schemas
from app.crud.crud_pdf_document import crud_pdf_document
from app.api import deps
from app.utils import utils

router = APIRouter()


@router.post("/", response_model=schemas.PDFDocument)
async def upload_pdf_document(
    title: str = Form(...),
    link: str = Form(...),
    category_id: int = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document_in = schemas.PDFDocumentCreate(
        title=title, link=link, category_id=category_id
    )
    document = crud_pdf_document.create_document(
        db=db, document=document_in, user_id=current_user.id
    )
    return document


@router.get("/all", response_model=list[schemas.PDFDocument])
def read_documents(
    skip: int = 0, limit: int = 2000, db: Session = Depends(deps.get_db)
):
    documents = crud_pdf_document.get_documents(db, skip=skip, limit=limit)
    return documents


@router.get("/{document_id}", response_model=schemas.PDFDocument)
def get_pdf_document_by_id(document_id: int, db: Session = Depends(deps.get_db)):
    document = crud_pdf_document.get_document_by_id(db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/category/{category_id}", response_model=list[schemas.PDFDocument])
def get_pdf_documents_by_category(category_id: int, db: Session = Depends(deps.get_db)):
    documents = crud_pdf_document.get_documents_by_category(db, category_id=category_id)
    return documents


@router.put("/{document_id}", response_model=schemas.PDFDocument)
async def update_pdf_document(
    document_id: int,
    title: str = Form(...),
    link: str = Form(...),
    category_id: int = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document = crud_pdf_document.get_document_by_id(db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    document_in = schemas.PDFDocumentUpdate(
        title=title, link=link, category_id=category_id
    )
    updated_document = crud_pdf_document.update_document(
        db=db, document_id=document_id, document=document_in
    )
    return updated_document


@router.delete("/{document_id}", response_model=schemas.PDFDocument)
def delete_pdf_document(
    document_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document = crud_pdf_document.get_document_by_id(db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this document"
        )
    return crud_pdf_document.delete_document(db, document_id=document_id)
