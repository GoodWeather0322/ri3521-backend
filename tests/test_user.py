# def test_create_user(test_client):
#     response = test_client.post(
#         "/users/",
#         json={"username": "testuser", "password": "testpassword"}
#     )
#     assert response.status_code == 200
#     assert response.json()["username"] == "testuser"

def test_login_user(test_client):
    response = test_client.post(
        "/login/access-token",
        data={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_token_decode(test_client):
    response = test_client.post(
        "/login/access-token",
        data={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    token = response.json()["access_token"]

    # 解碼 token
    from app.core.config import settings
    from jose import jwt
    from datetime import datetime, timedelta
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "admin"

    # 將 exp 轉換為 datetime 物件
    exp_timestamp = payload["exp"]
    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    # 確認 token 過期時間在 datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) +-1分鐘內
    assert exp_datetime > datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) - timedelta(minutes=1)
    assert exp_datetime < datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) + timedelta(minutes=1)
