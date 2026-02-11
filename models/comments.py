from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.extensions import db

if TYPE_CHECKING:
  from models.user import User
  from models.blogpost import BlogPost

class Comment(db.Model):
  __tablename__ = "comments"
  
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  text: Mapped[str]
  
  author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
  
  author: Mapped["User"] = relationship(back_populates="comments")
  parent_post: Mapped["BlogPost"] = relationship(back_populates="comments")