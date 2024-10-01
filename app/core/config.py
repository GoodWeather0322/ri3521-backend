# app/core/config.py
import secrets
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI App"
    DATABASE_URL: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @field_validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if not v or len(v) < 32:  # 檢查 SECRET_KEY 是否存在且長度是否小於32
            user_input = (
                v if v else secrets.token_urlsafe(16)
            )  # 使用者輸入或生成16字符長度的隨機URL安全密鑰
            return user_input + secrets.token_urlsafe(
                16
            )  # 融合使用者輸入和新的16字符長度的隨機URL安全密鑰
        return v

    class Config:
        env_file = ".env"


settings = Settings()
