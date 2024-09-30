# app/utils/utils.py
import os
import shutil
from fastapi import UploadFile
import uuid


def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    filename = f"{uuid.uuid4()}_{upload_file.filename}"
    destination = os.path.join(destination, filename)
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return destination
