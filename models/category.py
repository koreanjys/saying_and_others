# models/category.py

from sqlmodel import SQLModel, Field
from typing import List, Optional

class Category(SQLModel, table=True):  # 카테고리 테이블 모델 클래스
    id: Optional[int] = Field(default=None, primary_key=True)
    fourchar_categories: Optional[str] = None
    saying_categories: Optional[str] = None