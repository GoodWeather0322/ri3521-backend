from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.crud.crud_category import get_categories
from app.api import deps

router = APIRouter()


@router.get("/categories", response_model=list[schemas.Category])
def read_categories(
    skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)
):
    categories = get_categories(db, skip=skip, limit=limit)
    return categories
