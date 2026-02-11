from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.extensions import db

if TYPE_CHECKING:
  from models.user import User
  from models.comments import Comment

class BlogPost(db.Model):
  __tablename__ = "posts"
  
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  title: Mapped[str]
  subtitle: Mapped[str] 
  body: Mapped[str]
  date: Mapped[str]
  img_url: Mapped[str]
                                  
  author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  
  author: Mapped["User"] = relationship(back_populates="posts")
  comments: Mapped[list["Comment"]] = relationship(back_populates="parent_post", cascade="all, delete-orphan")