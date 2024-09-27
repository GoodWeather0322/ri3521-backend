# app/utils/init_data.py
from fastapi.testclient import TestClient
from fastapi import FastAPI


def create_admin_user(app: FastAPI):
    client = TestClient(app)
    response = client.post("/users/", json={"username": "admin", "password": "admin"})
    if (
        response.status_code == 400
        and response.json().get("detail") == "使用者名稱已被註冊"
    ):
        print("Admin user already exists.")
    elif response.status_code == 200:
        print("Admin user created successfully.")
    else:
        print("Failed to create admin user:", response.json())
