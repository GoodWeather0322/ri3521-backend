# app/api/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import crud_user
from app.api import deps

router = APIRouter()


@router.get("/verify", response_model=schemas.UserBase)
async def verify_token(current_user: models.User = Depends(deps.get_current_user)):
    return schemas.UserBase(username=current_user.username)
