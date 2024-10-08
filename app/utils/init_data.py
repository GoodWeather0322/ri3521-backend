# app/utils/init_data.py
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud import crud_user, crud_category
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


def init_categories():
    db: Session = SessionLocal()
    try:
        categories = [
            {"main_category": "RI資訊", "sub_category": "RI社長文告"},
            {"main_category": "地區資訊", "sub_category": "總監月刊"},
            {"main_category": "地區資訊", "sub_category": "總監的話"},
            {"main_category": "青年服務", "sub_category": "青年領袖營-RYLA"},
            {"main_category": "青年服務", "sub_category": "青少年交換委員會-RYE"},
            {"main_category": "青年服務", "sub_category": "新世代服務交換-NGSE"},
            {"main_category": "青年服務", "sub_category": "扶青社-Rotaract"},
            {"main_category": "青年服務", "sub_category": "扶少團-Interact"},
            {"main_category": "地區活動", "sub_category": "社長秘書聯席會"},
            {"main_category": "地區活動", "sub_category": "地區幹事研習會"},
            {"main_category": "地區活動", "sub_category": "GMS獎助金管理研習會"},
            {"main_category": "地區活動", "sub_category": "PETS社長當選人研習會"},
            {"main_category": "地區活動", "sub_category": "DTTS團隊訓練研習會"},
            {"main_category": "地區活動", "sub_category": "DLS地區領導入研習會"},
            {"main_category": "地區活動", "sub_category": "DTA地區訓練講習會"},
            {"main_category": "地區活動", "sub_category": "DMS社員發展研習會"},
            {"main_category": "地區活動", "sub_category": "DRFS扶輪基金研習會"},
            {"main_category": "地區活動", "sub_category": "服務計畫"},
            {"main_category": "地區活動", "sub_category": "地區年會"},
            {"main_category": "地區活動", "sub_category": "地區活動預告"},
            {"main_category": "眷聯誼會", "sub_category": "眷聯誼會活動"},
        ]

        for category in categories:
            existing_category = crud_category.get_category_by_main_and_sub(
                db,
                main_category=category["main_category"],
                sub_category=category["sub_category"],
            )
            if not existing_category:
                category_in = schemas.CategoryCreate(
                    main_category=category["main_category"],
                    sub_category=category["sub_category"],
                )
                crud_category.create_category(db, category=category_in)
                logger.info(
                    f"Category {category['main_category']} - {category['sub_category']} created successfully."
                )
            else:
                logger.info(
                    f"Category {category['main_category']} - {category['sub_category']} already exists."
                )
    finally:
        db.close()
