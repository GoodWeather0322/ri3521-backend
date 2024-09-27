# app/api/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import crud_user
from app.api import deps

router = APIRouter()


@router.get("/verify", response_model=schemas.UserBase)
def verify_user(username: str, db: Session = Depends(deps.get_db)):
    user = crud_user.get_user_by_username(db, username)
    if user:
        return schemas.UserBase(username=username)
    else:
        raise HTTPException(status_code=404, detail="使用者不存在")
