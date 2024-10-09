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

# 2. GET 所有 news、pdf_documents
news_url = f"{api_url}/api/news/all"
pdf_documents_url = f"{api_url}/api/documents/all"

params = {"skip": 0, "limit": 500}  # 起始位置  # 返回的最大項目數

news_response = requests.get(news_url, params=params, headers=headers)
pdf_documents_response = requests.get(pdf_documents_url, params=params, headers=headers)


news_items = news_response.json()
pdf_documents_items = pdf_documents_response.json()

print("目前資料庫有：")
print("news: ", len(news_items))
print("pdf_documents: ", len(pdf_documents_items))

# 3. 使用他們的 ID 進行 DELETE
for news in news_items:
    news_id = news["id"]
    delete_news_url = f"{api_url}/api/news/{news_id}"
    requests.delete(delete_news_url, headers=headers)

for pdf_document in pdf_documents_items:
    pdf_document_id = pdf_document["id"]
    delete_pdf_document_url = f"{api_url}/api/documents/{pdf_document_id}"
    requests.delete(delete_pdf_document_url, headers=headers)


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


# get all categories
categories_url = f"{api_url}/api/categories/all"
categories_response = requests.get(categories_url, headers=headers)
categories_items = categories_response.json()


for category in categories_items:
    for i in range(8):
        title = f"this is fake {category['sub_category']} title {i}"
        link = f"https://drive.google.com/drive/u/0/folders/1PRe2IYJiCQH5xMYSXI2rfgIHZBuhz5Wr"
        data = {
            "title": title,
            "link": link,
            "category_id": category["id"],
        }
        upload_pdf_document_url = f"{api_url}/api/documents/"
        requests.post(upload_pdf_document_url, data=data, headers=headers)
