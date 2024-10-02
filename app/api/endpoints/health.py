from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api import deps


router = APIRouter()


@router.get("/health", tags=["healthcheck"])
async def healthcheck():
    return {"status": "ok"}


@router.get("/health/db", tags=["healthcheck"])
async def healthcheck_db(
    db: Session = Depends(deps.get_db),
):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except SQLAlchemyError as e:
        return {"status": "error", "message": str(e)}
