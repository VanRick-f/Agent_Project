from typing import Optional
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column
from app_database import Base

class User(Base):
    __tablename__ = 'user'  # 表名

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  #id: Mapped[int]表示“一个被 SQLAlchemy 映射、值类型为 int 的字段”
    email: Mapped[str] = mapped_column(String(100),unique=True,index=True)
    username: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(200))