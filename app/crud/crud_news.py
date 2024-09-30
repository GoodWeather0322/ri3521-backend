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


def get_news_by_id(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()


def update_news(
    db: Session, news_id: int, news: schemas.NewsUpdate, image_path: str = None
):
    db_news = get_news_by_id(db, news_id)
    if db_news:
        db_news.title = news.title
        db_news.content = news.content
        if image_path:
            db_news.image_path = image_path
        db.commit()
        db.refresh(db_news)
    return db_news


def delete_news(db: Session, news_id: int):
    db_news = get_news_by_id(db, news_id)
    if db_news:
        db.delete(db_news)
        db.commit()
    return db_news
