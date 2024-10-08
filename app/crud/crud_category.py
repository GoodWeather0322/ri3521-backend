from sqlalchemy.orm import Session
from app.models import Category
from app.schemas import schemas


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = Category(
        main_category=category.main_category, sub_category=category.sub_category
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()


def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_main_and_sub(db: Session, main_category: str, sub_category: str):
    return (
        db.query(Category)
        .filter(
            Category.main_category == main_category,
            Category.sub_category == sub_category,
        )
        .first()
    )
