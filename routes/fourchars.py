# routes/fourchars.py

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlmodel import select, delete, func, or_, and_
from typing import List, Optional
from datetime import datetime, timedelta

from models.fourchars import FourChar, FourCharUpdate
from models.category import Category
from tools.pagination import paging

from database.connection import get_session


fourchar_router = APIRouter(tags=["FourChars"])


## CRUD START ############################################################################################## 

@fourchar_router.get("", response_model=dict)  # GET READ 모든 사자성어 데이터들
async def retrieve_all_fourchars(p: int=Query(default=1), size: int=Query(default=15), session=Depends(get_session)) -> dict:

    """
    저장된 모든 사자성어들 조회
    """
    # 토탈페이지 확인
    total_record = session.exec(select(func.count(FourChar.id))).one()
    total_page = (total_record // size) + bool(total_record % size)
    if p > total_page:
        p = total_page
    
    # 페이징 처리
    statement = select(FourChar)
    statement = paging(page=p, size=size, Table=FourChar, statement=statement)
    fourchars = session.exec(statement).all()

    return {
        "total_rows": total_record,
        "total_page": total_page,
        "content": fourchars
    }


@fourchar_router.get("/{id}", response_model=FourChar)  # GET READ 단일 사자성어 데이터
async def retrieve_fourchar(id: int, session=Depends(get_session)) -> FourChar:
    """
    사자성어 조회
    """
    fourchar = session.get(FourChar, id)
    if fourchar:
        return fourchar
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 사자성어가 존재하지 않습니다."
    )


@fourchar_router.post("/new", response_model=FourChar)  # POST CREATE 새 사자성어 데이터
async def create_new_fourchar(new_fourchar: FourChar, session=Depends(get_session)) -> FourChar:
    """
    사자성어 새로 생성
    """
    category_name = new_fourchar.category

    statement = select(Category).where(Category.fourchar_categories == category_name)
    category = session.exec(statement).first()

    if not category:
        category = Category(fourchar_categories=category_name)
        session.add(category)
        session.commit()
        session.refresh(category)

    session.add(new_fourchar)
    session.commit()
    session.refresh(new_fourchar)  # 캐시 데이터 업데이트
    return new_fourchar


@fourchar_router.put("/edit/{id}", response_model=FourChar)  # PUT UPDATE 기존 사자성어 데이터
async def update_fourchar(id: int, new_data: FourCharUpdate, session=Depends(get_session)) -> FourChar:
    """
    사자성어 수정
    """
    fourchar = session.get(FourChar, id)
    if fourchar:
        fourchar_data = new_data.model_dump(exclude_unset=True)  # 클라이언트가 작성한 데이터만 변경하는 dict 생성
        fourchar_data["updated_at"] = (datetime.utcnow() + timedelta(hours=9)).replace(microsecond=0)  # updated_at 컬럼에 업데이트 시간 추가
        for key, value in fourchar_data.items():
            setattr(fourchar, key, value)  # setattr(object, name, value) >>> object에 존재하는 속성의 값을 바꾸거나, 새로운 속성을 생성하여 값을 부여한다.
        session.add(fourchar)
        session.commit()
        session.refresh(fourchar)
        return fourchar
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 사자성어가 존재하지 않습니다."
    )

@fourchar_router.delete("/delete/{id}")  # DELETE 기존 사자성어 데이터
async def delete_fourchar(id: int, session=Depends(get_session)) -> dict:
    """
    사자성어 삭제
    """
    fourchar = session.get(FourChar, id)
    if fourchar:
        session.delete(fourchar)
        session.commit()
        return {
            "message": "사자성어를 삭제했습니다."
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 사자성어가 존재하지 않습니다."
    )
## CRUD END ##############################################################################################

# 필터링 라우터 함수
"""
카테고리들(List), 검색어(Str), 초성 첫글자들(List)
필터링 해주는 함수
"""
@fourchar_router.get("/filter/", response_model=dict)
async def fourchar_filtering(
        categories: List[str]=Query(default=None),
        keyword: str=Query(default=None),
        consonants: List[str]=Query(default=None),
        p: int=Query(default=1),
        size: int=Query(default=15),
        session=Depends(get_session)
        ) -> dict:
    
    statement = select(FourChar)

    if categories:  # 카테고리 필터가 됐다면,
        conditions = [FourChar.category==cat for cat in categories]
        statement = statement.where(or_(*conditions))

    if keyword:  # 검색어 필터가 됐다면,
        statement = statement.where(or_(FourChar.contents_detail.like(f"%{keyword}%"), FourChar.contents_kr.like(f"%{keyword}%"), FourChar.contents_zh.like(f"%{keyword}%")))

    if consonants:  # 초성 필터가 됐다면,
        ranges = {
                "ㄱ": ("가", "나"),
                "ㄴ": ("나", "다"),
                "ㄷ": ("다", "라"),
                "ㄹ": ("라", "마"),
                "ㅁ": ("마", "바"),
                "ㅂ": ("바", "사"),
                "ㅅ": ("사", "아"),
                "ㅇ": ("아", "자"),
                "ㅈ": ("자", "차"),
                "ㅊ": ("차", "카"),
                "ㅋ": ("카", "타"),
                "ㅌ": ("타", "파"),
                "ㅍ": ("파", "하"),
                "ㅎ": ("하", "힣"),
                }
        conditions = [and_(ranges[consonant][0] <= FourChar.contents_kr, FourChar.contents_kr < ranges[consonant][1]) for consonant in consonants]
        statement = statement.where(or_(*conditions))

    # 토탈 페이지 확인
    total_record = session.exec(select(func.count()).select_from(statement)).one()
    total_page = (total_record // size) + bool(total_record % size)
    if p > total_page:
        p = total_page
    
    # 페이징 처리
    statement = paging(page=p, size=size, Table=FourChar, statement=statement)
    filtered_fourchars = session.exec(statement).all()

    return {
        "total_rows": total_record,
        "total_page": total_page,
        "content": filtered_fourchars
    }