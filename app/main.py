# app/main.py
from fastapi import FastAPI
from app.api import api
from app.db import models
from app.db.session import engine
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="My FastAPI App")

app.include_router(api.api_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
