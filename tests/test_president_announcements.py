def test_upload_president_announcement(test_client, test_user_token):
    # 模擬檔案上傳
    file_path = "tests/assets/test_president_announcement.txt"
    with open(file_path, "w") as f:
        f.write("This is a test president announcement.")

    with open(file_path, "rb") as f:
        response = test_client.post(
            "/api/president_announcements/",
            files={"file": ("test_president_announcement.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert response.status_code == 200
    file_path_response = response.json()["file_path"]
    assert file_path_response.startswith("app/static/president_announcements")
    assert "test_president_announcement.txt" in file_path_response


def test_read_president_announcement_by_id(test_client, test_user_token):
    # 模擬檔案上傳
    file_path = "tests/assets/test_president_announcement.txt"
    file_content = "This is a test president announcement."
    with open(file_path, "w") as f:
        f.write(file_content)

    with open(file_path, "rb") as f:
        upload_response = test_client.post(
            "/api/president_announcements/",
            files={"file": ("test_president_announcement.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert upload_response.status_code == 200
    document_id = upload_response.json()["id"]

    # 讀取檔案
    response = test_client.get(
        f"/api/president_announcements/{document_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == document_id
    assert response.json()["file_path"].startswith("app/static/president_announcements")
    assert "test_president_announcement.txt" in response.json()["file_path"]
    assert response.json()["file"] == file_content


def test_update_president_announcement(test_client, test_user_token):
    # 模擬檔案上傳
    file_path = "tests/assets/test_president_announcement.txt"
    with open(file_path, "w") as f:
        f.write("This is a test president announcement.")

    with open(file_path, "rb") as f:
        upload_response = test_client.post(
            "/api/president_announcements/",
            files={"file": ("test_president_announcement.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert upload_response.status_code == 200
    document_id = upload_response.json()["id"]

    # 更新檔案
    new_file_path = "tests/assets/updated_test_president_announcement.txt"
    with open(new_file_path, "w") as f:
        f.write("This is an updated test president announcement.")

    with open(new_file_path, "rb") as f:
        update_response = test_client.put(
            f"/api/president_announcements/{document_id}",
            files={
                "file": ("updated_test_president_announcement.txt", f, "text/plain")
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert update_response.status_code == 200
    updated_file_path_response = update_response.json()["file_path"]
    assert updated_file_path_response.startswith("app/static/president_announcements")
    assert "updated_test_president_announcement.txt" in updated_file_path_response


def test_delete_president_announcement(test_client, test_user_token):
    # 模擬檔案上傳
    file_path = "tests/assets/test_president_announcement_to_delete.txt"
    with open(file_path, "w") as f:
        f.write("This document will be deleted.")

    with open(file_path, "rb") as f:
        upload_response = test_client.post(
            "/api/president_announcements/",
            files={
                "file": ("test_president_announcement_to_delete.txt", f, "text/plain")
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert upload_response.status_code == 200
    document_id = upload_response.json()["id"]

    # 刪除檔案
    delete_response = test_client.delete(
        f"/api/president_announcements/{document_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert delete_response.status_code == 200

    # 確認檔案已被刪除
    get_response = test_client.get(
        f"/api/president_announcements/{document_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert get_response.status_code == 404
