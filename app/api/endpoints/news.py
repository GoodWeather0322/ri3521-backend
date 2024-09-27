# app/api/endpoints/news.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas import schemas
from app.crud import crud_news
from app.api import deps
from app.utils import utils

router = APIRouter()


@router.post("/", response_model=schemas.News)
async def create_news(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    image_filename = image.filename
    image_path = f"app/static/images/{image_filename}"
    utils.save_upload_file(image, image_path)
    news_in = schemas.NewsCreate(title=title, content=content)
    news_item = crud_news.create_news(
        db=db, news=news_in, image_path=image_path, user_id=current_user.id
    )
    return news_item


@router.get("/", response_model=list[schemas.News])
def read_news(skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)):
    news_items = crud_news.get_news(db, skip=skip, limit=limit)
    return news_items
