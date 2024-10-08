# app/models/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    news = relationship("News", back_populates="owner")
    director_messages = relationship("DirectorMessage", back_populates="owner")
    president_announcements = relationship(
        "PresidentAnnouncement", back_populates="owner"
    )
    pdf_documents = relationship("PDFDocument", back_populates="owner")


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    title = Column(String(255))
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="news")


class BaseDocument(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey("users.id"))

    @declared_attr
    def owner(cls):
        return relationship("User")


class DirectorMessage(BaseDocument):
    __tablename__ = "director_messages"


class PresidentAnnouncement(BaseDocument):
    __tablename__ = "president_announcements"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    main_category = Column(String(255), nullable=False)
    sub_category = Column(String(255), nullable=False)

    pdf_documents = relationship("PDFDocument", back_populates="category")


class PDFDocument(Base):
    __tablename__ = "pdf_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="pdf_documents")
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="pdf_documents")
