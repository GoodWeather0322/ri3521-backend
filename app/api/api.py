# app/api/api.py
from fastapi import APIRouter
from app.api.endpoints import (
    news,
    director_messages,
    president_announcements,
    users,
    login,
)

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(
    director_messages.router, prefix="/director_messages", tags=["director_messages"]
)
api_router.include_router(
    president_announcements.router,
    prefix="/president_announcements",
    tags=["president_announcements"],
)
