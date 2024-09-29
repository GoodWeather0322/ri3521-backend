def test_upload_document(test_client, test_user_token):
    # 模擬文件上傳
    file_path = "tests/assets/test_document.txt"
    with open(file_path, "w") as f:
        f.write("This is a test document.")

    with open(file_path, "rb") as f:
        response = test_client.post(
            "/documents/",
            files={"file": ("test_document.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert response.status_code == 200
    assert response.json()["file_path"] == "app/static/documents/test_document.txt"
