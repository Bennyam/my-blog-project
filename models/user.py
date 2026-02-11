from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from utils.extensions import db

if TYPE_CHECKING:
  from models.blogpost import BlogPost
  from models.comments import Comment

class User(UserMixin, db.Model):
  __tablename__ = "users"
  
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str]
  email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
  password: Mapped[str]
  is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
  
  comments: Mapped[list["Comment"]] = relationship(back_populates="author", cascade="all, delete-orphan")
  posts: Mapped[list["BlogPost"]] = relationship(back_populates="author", cascade="all, delete-orphan")