# app/api/api.py
from fastapi import APIRouter
from app.api.endpoints import news, documents, users, login

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
