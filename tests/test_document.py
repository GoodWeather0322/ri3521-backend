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


def test_delete_document(test_client, test_user_token):
    # 模擬文件上傳
    file_path = "tests/assets/test_document_to_delete.txt"
    with open(file_path, "w") as f:
        f.write("This document will be deleted.")

    with open(file_path, "rb") as f:
        upload_response = test_client.post(
            "/documents/",
            files={"file": ("test_document_to_delete.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert upload_response.status_code == 200
    document_id = upload_response.json()["id"]

    # 刪除文件
    delete_response = test_client.delete(
        f"/documents/{document_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert delete_response.status_code == 200

    # 確認文件已被刪除
    get_response = test_client.get(
        f"/documents/{document_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert get_response.status_code == 404
