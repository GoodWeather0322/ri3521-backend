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
