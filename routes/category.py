# routes/category.py

from fastapi import APIRouter, Depends, Query
from sqlmodel import select
from typing import List

from models.category import Category
from models.sayings import Saying
from models.fourchars import FourChar

from database.connection import get_session


category_router = APIRouter(tags=["Category"])


@category_router.get("/")  # GET READ 모든 select_category(saying or fourchar)의 카테고리들
async def retrieve_all_categories(select_category: str=Query(default=None), session=Depends(get_session)):
    if select_category == "fourchar":
        statement = select(Category.fourchar_categories).where(Category.fourchar_categories.isnot(None)).order_by(Category.fourchar_categories.asc())
    else:
        statement = select(Category.saying_categories).where(Category.saying_categories.isnot(None)).order_by(Category.saying_categories.asc())
    categories = session.exec(statement).all()
    return categories


# 카테고리 테이블 업데이트 URL
"""
/category/new_all 에 접속만 해도 자동으로 카테고리 테이블 요소들을 생성
"""
@category_router.get("/new_all")
async def new_all_categories(session=Depends(get_session)) -> dict:
    """
    카테고리 테이블의 데이터를 업데이트 합니다.
    """
    # 명언 데이터의 카테고리 불러오기 & category_set에 데이터 넣기
    statement = select(Saying.category).distinct()
    saying_categories = session.exec(statement).all()
    
    # 사자성어 데이터의 카테고리 불러오기 & category_set에 데이터 넣기
    statement = select(FourChar.category).distinct()
    fourchar_categories = session.exec(statement).all()

    for cat in saying_categories:
        saying_category = Category(saying_categories=cat)
        session.add(saying_category)
    
    for cat in fourchar_categories:
        fourchar_category = Category(fourchar_categories=cat)
        session.add(fourchar_category)
    
    session.commit()
    return {
        "message": "카테고리 업데이트 했습니다."
    }