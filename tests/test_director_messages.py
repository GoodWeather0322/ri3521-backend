def test_upload_director_message(test_client, test_user_token):
    # 模擬文件上傳
    file_path = "tests/assets/test_director_message.txt"
    with open(file_path, "w") as f:
        f.write("This is a test director message.")

    with open(file_path, "rb") as f:
        response = test_client.post(
            "/director_messages/",
            files={"file": ("test_director_message.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert response.status_code == 200
    file_path_response = response.json()["file_path"]
    assert file_path_response.startswith("app/static/director_messages")
    assert "test_director_message.txt" in file_path_response


def test_update_director_message(test_client, test_user_token):
    # 模擬文件上傳
    file_path = "tests/assets/test_director_message.txt"
    with open(file_path, "w") as f:
        f.write("This is a test director message.")

    with open(file_path, "rb") as f:
        upload_response = test_client.post(
            "/director_messages/",
            files={"file": ("test_director_message.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert upload_response.status_code == 200
    document_id = upload_response.json()["id"]

    # 更新文件
    new_file_path = "tests/assets/updated_test_director_message.txt"
    with open(new_file_path, "w") as f:
        f.write("This is an updated test director message.")

    with open(new_file_path, "rb") as f:
        update_response = test_client.put(
            f"/director_messages/{document_id}",
            files={"file": ("updated_test_director_message.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert update_response.status_code == 200
    updated_file_path_response = update_response.json()["file_path"]
    assert updated_file_path_response.startswith("app/static/director_messages")
    assert "updated_test_director_message.txt" in updated_file_path_response


def test_delete_director_message(test_client, test_user_token):
    # 模擬文件上傳
    file_path = "tests/assets/test_director_message_to_delete.txt"
    with open(file_path, "w") as f:
        f.write("This document will be deleted.")

    with open(file_path, "rb") as f:
        upload_response = test_client.post(
            "/director_messages/",
            files={"file": ("test_director_message_to_delete.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert upload_response.status_code == 200
    document_id = upload_response.json()["id"]

    # 刪除文件
    delete_response = test_client.delete(
        f"/director_messages/{document_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert delete_response.status_code == 200

    # 確認文件已被刪除
    get_response = test_client.get(
        f"/director_messages/{document_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert get_response.status_code == 404
