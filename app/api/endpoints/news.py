# app/api/endpoints/news.py
import io
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
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
    image_path = "app/static/images"
    saved_path = utils.save_upload_file(image, image_path)
    news_in = schemas.NewsCreate(title=title, content=content)
    news_item = crud_news.create_news(
        db=db, news=news_in, image_path=saved_path, user_id=current_user.id
    )
    return news_item


@router.get("/all", response_model=list[schemas.News])
def read_news(skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)):
    news_items = crud_news.get_news(db, skip=skip, limit=limit)
    return news_items


@router.get("/{news_id}/image", response_class=StreamingResponse)
def get_news_image(news_id: int, db: Session = Depends(deps.get_db)):
    news_item = crud_news.get_news_by_id(db, news_id=news_id)
    if not news_item:
        raise HTTPException(status_code=404, detail="News not found")
    # 讀取圖片檔案
    file_path = news_item.image_path
    with open(file_path, "rb") as file:
        file_content = file.read()
    return StreamingResponse(io.BytesIO(file_content), media_type="image/jpeg")


@router.put("/{news_id}", response_model=schemas.News)
async def update_news(
    news_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),  # 允許圖片為空
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

    # 更新圖片
    saved_path = None
    if image:
        image_path = "app/static/images"
        saved_path = utils.save_upload_file(image, image_path)

    # 更新新聞
    news_in = schemas.NewsUpdate(title=title, content=content)

    return crud_news.update_news(
        db=db, news_id=news_id, news=news_in, image_path=saved_path
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
