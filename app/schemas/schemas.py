# app/schemas/schemas.py
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class NewsBase(BaseModel):
    title: str
    content: str


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsBase):
    pass


class News(NewsBase):
    id: int
    image_path: str
    created_at: datetime

    class Config:
        from_attributes = True


class BaseDocument(BaseModel):
    id: int
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class DocumentWithFile(BaseDocument):
    file: bytes


class DirectorMessage(BaseDocument):
    pass


class PresidentAnnouncement(BaseDocument):
    pass


class CategoryBase(BaseModel):
    main_category: str
    sub_category: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class PDFDocumentBase(BaseModel):
    title: str
    link: str
    category_id: int


class PDFDocumentCreate(PDFDocumentBase):
    pass


class PDFDocumentUpdate(PDFDocumentBase):
    pass


class PDFDocument(PDFDocumentBase):
    id: int
    upload_time: datetime
    category: Category

    class Config:
        orm_mode = True
