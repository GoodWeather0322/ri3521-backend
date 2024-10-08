def test_create_news(test_client, test_user_token):
    response = test_client.post(
        "/api/news/",
        data={"title": "Test News", "content": "This is a test news content."},
        files={"image": ("test_image.jpg", b"fake image data", "image/jpeg")},
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test News"
    assert response.json()["content"] == "This is a test news content."


def test_read_news(test_client):
    response = test_client.get("/api/news/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_news_by_id(test_client, test_user_token):
    # 創建一個最新消息
    create_response = test_client.post(
        "/api/news/",
        data={"title": "Test News", "content": "This is a test news content."},
        files={"image": ("test_image.jpg", b"fake image data", "image/jpeg")},
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert create_response.status_code == 200
    news_id = create_response.json()["id"]

    # 讀取最新消息
    response = test_client.get(
        f"/api/news/{news_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 200
    news_data = response.json()
    assert news_data["title"] == "Test News"
    assert news_data["content"] == "This is a test news content."
    assert "image" in news_data
    assert news_data["image"] == "fake image data"


def test_update_news(test_client, test_user_token):
    # 創建一個最新消息
    create_response = test_client.post(
        "/api/news/",
        data={"title": "Test News", "content": "This is a test news content."},
        files={"image": ("test_image.jpg", b"fake image data", "image/jpeg")},
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    news_id = create_response.json()["id"]

    # 更新最新消息
    response = test_client.put(
        f"/api/news/{news_id}",
        data={
            "title": "Updated Test News",
            "content": "This is an updated test news content.",
        },
        files={
            "image": (
                "updated_test_image.jpg",
                b"updated fake image data",
                "image/jpeg",
            )
        },
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test News"
    assert response.json()["content"] == "This is an updated test news content."


def test_delete_news(test_client, test_user_token):
    # 創建一個最新消息
    create_response = test_client.post(
        "/api/news/",
        data={"title": "Test News", "content": "This is a test news content."},
        files={"image": ("test_image.jpg", b"fake image data", "image/jpeg")},
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    news_id = create_response.json()["id"]

    # 刪除最新消息
    response = test_client.delete(
        f"/api/news/{news_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 200

    # 確認最新消息已被刪除
    get_response = test_client.get(f"/api/news/{news_id}")
    assert get_response.status_code == 404
