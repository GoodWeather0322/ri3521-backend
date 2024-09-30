def test_upload_president_announcement(test_client, test_user_token):
    # 模擬文件上傳
    file_path = "tests/assets/test_president_announcement.txt"
    with open(file_path, "w") as f:
        f.write("This is a test president announcement.")

    with open(file_path, "rb") as f:
        response = test_client.post(
            "/president_announcements/",
            files={"file": ("test_president_announcement.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert response.status_code == 200
    file_path_response = response.json()["file_path"]
    assert file_path_response.startswith("app/static/president_announcements")
    assert "test_president_announcement.txt" in file_path_response


def test_delete_president_announcement(test_client, test_user_token):
    # 模擬文件上傳
    file_path = "tests/assets/test_president_announcement_to_delete.txt"
    with open(file_path, "w") as f:
        f.write("This document will be deleted.")

    with open(file_path, "rb") as f:
        upload_response = test_client.post(
            "/president_announcements/",
            files={
                "file": ("test_president_announcement_to_delete.txt", f, "text/plain")
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
    assert upload_response.status_code == 200
    document_id = upload_response.json()["id"]

    # 刪除文件
    delete_response = test_client.delete(
        f"/president_announcements/{document_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert delete_response.status_code == 200

    # 確認文件已被刪除
    get_response = test_client.get(
        f"/president_announcements/{document_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert get_response.status_code == 404
