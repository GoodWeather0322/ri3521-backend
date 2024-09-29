# app/utils/init_data.py
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud import crud_user
from app.schemas import schemas
from app.core.logging_config import logging

logger = logging.getLogger(__name__)


def create_admin_user():
    db: Session = SessionLocal()
    try:
        admin_user = crud_user.get_user_by_username(db, username="admin")
        if not admin_user:
            admin_user_in = schemas.UserCreate(username="admin", password="admin")
            crud_user.create_user(db, user=admin_user_in)
            logger.info("Admin user created successfully.")
        else:
            logger.info("Admin user already exists.")
    finally:
        db.close()
