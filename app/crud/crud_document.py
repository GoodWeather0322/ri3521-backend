# app/crud/crud_document.py
from sqlalchemy.orm import Session
from app import models, schemas


def create_document(db: Session, file_path: str, user_id: int):
    db_document = models.KnowledgeDocument(file_path=file_path, user_id=user_id)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def get_documents(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.KnowledgeDocument).offset(skip).limit(limit).all()


def delete_document(db: Session, document_id: int):
    document = __get_document_by_id(db, document_id)
    if document:
        db.delete(document)
        db.commit()
    return document


def __get_document_by_id(db: Session, document_id: int):
    return (
        db.query(models.KnowledgeDocument)
        .filter(models.KnowledgeDocument.id == document_id)
        .first()
    )
