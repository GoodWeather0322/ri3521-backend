from sqlalchemy.orm import Session
from app.models import PDFDocument
from app.crud.crud_base_document import CRUDBaseDocument
from app.schemas import schemas


class CRUDPDFDocument(CRUDBaseDocument):
    model = PDFDocument

    def create_document(
        self, db: Session, document: schemas.PDFDocumentCreate, user_id: int
    ):
        db_document = self.model(
            title=document.title,
            link=document.link,
            category_id=document.category_id,
            user_id=user_id,
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        return db_document

    def update_document(
        self, db: Session, document_id: int, document: schemas.PDFDocumentUpdate
    ):
        db_document = self.get_document_by_id(db, document_id)
        if db_document:
            db_document.title = document.title
            db_document.link = document.link
            db_document.category_id = document.category_id
            db.commit()
            db.refresh(db_document)
        return db_document

    def get_documents_by_category(self, db: Session, category_id: int):
        return db.query(self.model).filter(self.model.category_id == category_id).all()


crud_pdf_document = CRUDPDFDocument()
