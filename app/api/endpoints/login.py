# app/api/endpoints/login.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.models import models
from app.core.config import settings
from app.utils.security import verify_password, create_access_token

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = deps.get_user(db, username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="使用者名稱或密碼錯誤")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="使用者名稱或密碼錯誤")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
