from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["healthcheck"])
async def healthcheck():
    return {"status": "ok"}


@router.get("/health/db", tags=["healthcheck"])
async def healthcheck_db():
    try:
        from app.db.session import get_db
        from sqlalchemy.exc import SQLAlchemyError

        db = next(get_db())
        db.execute("SELECT 1")
        return {"status": "ok"}
    except SQLAlchemyError as e:
        return {"status": "error", "message": str(e)}
