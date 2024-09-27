# app/crud/crud_news.py
from sqlalchemy.orm import Session
from app import models, schemas


def create_news(db: Session, news: schemas.NewsCreate, image_path: str, user_id: int):
    db_news = models.News(
        title=news.title, content=news.content, image_path=image_path, user_id=user_id
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


def get_news(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.News).offset(skip).limit(limit).all()
