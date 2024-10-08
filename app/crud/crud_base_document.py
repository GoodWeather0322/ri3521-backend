# app/crud/crud_document.py
from sqlalchemy.orm import Session, joinedload


class CRUDBaseDocument:
    model = None

    def create_document(self, db: Session, file_path: str, user_id: int):
        db_document = self.model(file_path=file_path, user_id=user_id)
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        return db_document

    def get_documents(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_document_by_id(self, db: Session, document_id: int):
        return (
            db.query(self.model)
            .options(joinedload(self.model.category))
            .filter(self.model.id == document_id)
            .first()
        )

    def update_document(self, db: Session, document_id: int, new_file_path: str):
        document = self.get_document_by_id(db, document_id)
        if document:
            document.file_path = new_file_path
            db.commit()
            db.refresh(document)
        return document

    def delete_document(self, db: Session, document_id: int):
        document = self.get_document_by_id(db, document_id)
        if document:
            db.delete(document)
            db.commit()
        return document
