# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import models
from app.api import api
from app.db.session import engine
from app.utils.init_data import create_admin_user


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="My FastAPI App")

app.include_router(api.api_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


# 應用啟動時創建 admin user
create_admin_user()
