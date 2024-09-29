import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jose import jwt
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.utils.security import create_access_token

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client

@pytest.fixture(scope="module")
def test_user_token():
    # 創建測試用戶的 token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": "admin"}, expires_delta=access_token_expires
    )
    return token
