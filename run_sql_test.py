import requests
from PyPDF2 import PdfWriter
from PIL import Image
import random
import os

api_url = "http://localhost:8000"
# 1. 透過帳號密碼取得 token
login_url = f"{api_url}/api/login/access-token"
login_data = {"username": "admin", "password": "admin"}
response = requests.post(login_url, data=login_data)
token = response.json().get("access_token")
print(token)
headers = {"Authorization": f"Bearer {token}"}

# 2. GET 所有 news、director_messages、president_announcements
news_url = f"{api_url}/api/news/all"
director_messages_url = f"{api_url}/api/director_messages/all"
president_announcements_url = f"{api_url}/api/president_announcements/all"

params = {"skip": 0, "limit": 100}  # 起始位置  # 返回的最大項目數

news_response = requests.get(news_url, params=params, headers=headers)
director_messages_response = requests.get(
    director_messages_url, params=params, headers=headers
)
president_announcements_response = requests.get(
    president_announcements_url, params=params, headers=headers
)

news_items = news_response.json()
director_messages_items = director_messages_response.json()
president_announcements_items = president_announcements_response.json()

print("目前資料庫有：")
print("news: ", len(news_items))
print("director_messages: ", len(director_messages_items))
print("president_announcements: ", len(president_announcements_items))

# 3. 使用他們的 ID 進行 DELETE
for news in news_items:
    news_id = news["id"]
    delete_news_url = f"{api_url}/api/news/{news_id}"
    requests.delete(delete_news_url, headers=headers)

for message in director_messages_items:
    message_id = message["id"]
    delete_message_url = f"{api_url}/api/director_messages/{message_id}"
    requests.delete(delete_message_url, headers=headers)

for announcement in president_announcements_items:
    announcement_id = announcement["id"]
    delete_announcement_url = f"{api_url}/api/president_announcements/{announcement_id}"
    requests.delete(delete_announcement_url, headers=headers)


def create_random_image(file_path: str, width: int = 100, height: int = 100):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image = Image.new("RGB", (width, height), color)
    image.save(file_path)


for i in range(1, 16):
    upload_file_path = f"news_{i}.jpg"
    create_random_image(upload_file_path)
    title = f"this is news title {i}"
    content = f"this is news content {i}"
    upload_news_url = f"{api_url}/api/news/"
    data = {
        "title": title,
        "content": content,
    }
    files = {"image": (upload_file_path, open(upload_file_path, "rb"), "image/jpeg")}
    requests.post(upload_news_url, data=data, files=files, headers=headers)
    os.remove(upload_file_path)


def create_fake_pdf(file_path: str, content: str):
    pdf_writer = PdfWriter()
    pdf_writer.add_blank_page(width=72, height=72)
    with open(file_path, "wb") as f:
        pdf_writer.write(f)


for i in range(1, 16):
    upload_file_path = f"director_messages_{i}.pdf"
    content = f"This is the {i}th director message."
    create_fake_pdf(upload_file_path, content)

    with open(upload_file_path, "rb") as file_bytes:
        files = {"file": (upload_file_path, file_bytes, "application/pdf")}
        upload_director_messages_url = f"{api_url}/api/director_messages/"
        requests.post(upload_director_messages_url, files=files, headers=headers)

    os.remove(upload_file_path)

for i in range(1, 16):
    upload_file_path = f"president_announcements_{i}.pdf"
    content = f"This is the {i}th president announcement."
    create_fake_pdf(upload_file_path, content)

    with open(upload_file_path, "rb") as file_bytes:
        files = {"file": (upload_file_path, file_bytes, "application/pdf")}
        upload_president_announcements_url = f"{api_url}/api/president_announcements/"
        requests.post(upload_president_announcements_url, files=files, headers=headers)

    os.remove(upload_file_path)
