# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import models
from app.api import api
from app.db.session import engine
from app.utils.init_data import create_admin_user


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ri3521-backend")

app.include_router(api.api_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


# 應用啟動時創建 admin user
create_admin_user()

# TODO: 牽涉到儲存檔名可能需要改成UUID儲存，避免使用者一直用重複檔名導致儲存的影像一直被複寫
# TODO: 可能需要資料庫對應儲存的UUID檔名與使用者上傳的檔名
