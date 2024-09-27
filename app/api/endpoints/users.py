# app/api/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import crud_user
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    user = crud_user.get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(status_code=400, detail="使用者名稱已被註冊")
    user = crud_user.create_user(db, user=user_in)
    return user
