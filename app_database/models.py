from typing import Optional
from sqlalchemy import Integer, String, Text,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app_database import Base 

class User(Base):
    __tablename__ = 'user'  # 表名

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  #id: Mapped[int]表示“一个被 SQLAlchemy 映射、值类型为 int 的字段”
    email: Mapped[str] = mapped_column(String(100),unique=True,index=True)
    username: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(200))

    user_extension: Mapped["UserExtension"] = relationship(back_populates="user", uselist=False)
    articles:Mapped[list["Article"]] = relationship(back_populates="author")



# 和User模型一对一关系
class UserExtension(Base):
    __tablename__ = 'user_extension'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    university: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"),unique = True)
    user: Mapped["User"] = relationship(back_populates="user_extension")

# 和User是一对多关系
class Article(Base):
    __tablename__ = 'article'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    author: Mapped["User"] = relationship( back_populates='articles')
    tags:Mapped[list['Tag']] = relationship(secondary="article_tag",back_populates='articles')
    

# 和Article是多对多关系
class Tag(Base):
    __tablename__ = 'tag'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    articles: Mapped[list["Article"]] = relationship(secondary="article_tag", back_populates='tags', lazy='dynamic')

# Article和Tag多对多关系的中间表
class ArticleTag(Base):
    __tablename__ = "article_tag"
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("article.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tag.id"), primary_key=True)