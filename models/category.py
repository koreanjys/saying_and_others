# models/category.py

from sqlmodel import SQLModel, Field
from typing import List, Optional

class Category(SQLModel, table=True):  # 카테고리 테이블 모델 클래스
    id: Optional[int] = Field(default=None, primary_key=True)
    fourchar_categories: Optional[str] = None
    saying_categories: Optional[str] = None


# 기존에 크롤링 데이터에 이미 카테고리 필드와 카테고리 필드 값이 입력이 되어 있어서 Relationship으로 작성하지 않음.
# 추후에 시간이 나면 수정
# 아래는 미리 만들어 둔 모델(추가 필드가 필요)
class FourcharCategory(SQLModel, table=True):  # 사자성어 카테고리
    id: Optional[int] = Field(default=None, primary_key=True)
    category: Optional[str] = None


class SayingCategory(SQLModel, table=True):  # 명언 카테고리
    id: Optional[int] = Field(default=True, primary_key=True)
    category: Optional[str] = None