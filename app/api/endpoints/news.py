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


@router.get("/all", response_model=list[schemas.News])
def read_news(skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)):
    news_items = crud_news.get_news(db, skip=skip, limit=limit)
    return news_items


@router.get("/{news_id}", response_model=schemas.News)
def read_news_by_id(news_id: int, db: Session = Depends(deps.get_db)):
    news_item = crud_news.get_news_by_id(db, news_id=news_id)
    if not news_item:
        raise HTTPException(status_code=404, detail="News not found")
    return news_item


@router.put("/{news_id}", response_model=schemas.News)
async def update_news(
    news_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),  # 允许图像文件为空
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    news_item = crud_news.get_news_by_id(db, news_id=news_id)
    if not news_item:
        raise HTTPException(status_code=404, detail="News not found")
    if news_item.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this news"
        )

    # 更新图像文件
    image_path = None
    if image:
        image_filename = image.filename
        image_path = f"app/static/images/{image_filename}"
        utils.save_upload_file(image, image_path)

    # 更新新闻
    news_in = schemas.NewsUpdate(title=title, content=content)

    return crud_news.update_news(
        db=db, news_id=news_id, news=news_in, image_path=image_path
    )


@router.delete("/{news_id}", response_model=schemas.News)
def delete_news(
    news_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    news_item = crud_news.get_news_by_id(db, news_id=news_id)
    if not news_item:
        raise HTTPException(status_code=404, detail="News not found")
    if news_item.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this news"
        )
    return crud_news.delete_news(db=db, news_id=news_id)
