# routes/sayings.py

from fastapi import APIRouter, HTTPException, status, Depends, Query, Body
from sqlmodel import select, delete, func, or_, and_
from typing import List, Optional
from datetime import datetime, timedelta

from models.sayings import Saying, SayingUpdate
from models.category import Category
from tools.pagination import paging
from tools.create_good_bad import create_good_bad

from database.connection import get_session


saying_router = APIRouter(tags=["Sayings"])


## CRUD START ############################################################################################## 

@saying_router.get("", response_model=dict)  # GET READ 모든 명언 데이터들
async def retrieve_all_sayings(p: int=Query(default=1), size: int=Query(default=15), session=Depends(get_session)) -> dict:
    """
    저장된 명언 데이터들 조회
    """
    # 토탈 페이지 확인
    total_record = session.exec(select(func.count(Saying.id))).one()
    total_page = (total_record // size) + bool(total_record % size)
    if p > total_page:
        p = total_page

    # 페이징 처리
    statement = select(Saying)
    statement = paging(page=p, size=size, Table=Saying, statement=statement)  # tools/pagination.py 페이지 처리 툴
    sayings = session.exec(statement).all()

    return {
        "total_rows": total_record,
        "total_page": total_page,
        "content": sayings
    }


@saying_router.get("/{id}", response_model=Saying)  # GET READ 단일 명언 데이터
async def retrieve_saying(id: int, session=Depends(get_session)) -> Saying:
    """
    데이터 조회
    """
    saying = session.get(Saying, id)
    if saying:
        return saying
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 데이터이 존재하지 않습니다."
    )


@saying_router.post("/new", response_model=Saying)  # POST CREATE 새 명언 데이터
async def create_new_saying(new_saying: Saying, session=Depends(get_session)) -> Saying:
    """
    데이터 새로 생성
    """
    category_name = new_saying.category

    statement = select(Category).where(Category.saying_categories == category_name)
    category = session.exec(statement).first()

    if not category:  # 카테고리명이 없으면 새로 생성
        category = Category(saying_categories=category_name)
        session.add(category)
        session.commit()
        session.refresh(category)

    session.add(new_saying)
    session.commit()
    session.refresh(new_saying)  # 캐시 데이터 업데이트
    return new_saying


@saying_router.put("/edit/{id}", response_model=Saying)  # PUT UPDATE 기존 명언 데이터
async def update_saying(id: int, new_data: SayingUpdate, session=Depends(get_session)) -> Saying:
    """
    데이터 수정
    """
    saying = session.get(Saying, id)
    if saying:
        saying_data = new_data.model_dump(exclude_unset=True)  # 클라이언트가 작성한 데이터만 변경하는 dict 생성
        saying_data["updated_at"] = (datetime.utcnow() + timedelta(hours=9)).replace(microsecond=0)  # updated_at 컬럼에 업데이트 시간을 작성
        for key, value in saying_data.items():
            setattr(saying, key, value)  # setattr(object, name, value) >>> object에 존재하는 속성의 값을 바꾸거나, 새로운 속성을 생성하여 값을 부여한다.
        session.add(saying)
        session.commit()
        session.refresh(saying)
        return saying
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 데이터이 존재하지 않습니다."
    )

@saying_router.delete("/delete/{id}")  # DELETE 기존 명언 데이터
async def delete_saying(id: int, session=Depends(get_session)) -> dict:
    """
    데이터 삭제
    """
    saying = session.get(Saying, id)
    if saying:
        session.delete(saying)
        session.commit()
        return {
            "message": "데이터을 삭제했습니다."
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 데이터가 존재하지 않습니다."
    )
## CRUD END ##############################################################################################

# 필터링 라우터 함수
"""
카테고리들(List), 검색어(Str), 알파벳 첫글자들(List)
필터링 해주는 함수
"""
@saying_router.get("/filter/", response_model=dict)
async def saying_filtering(
        categories: List[str]=Query(default=None),
        keyword: str=Query(default=None),
        consonants: List[str]=Query(default=None),
        p: int=Query(default=1),
        size: int=Query(default=15),
        isnull: int=Query(default=None),
        session=Depends(get_session)
        ) -> dict:

    statement = select(Saying)

    if isnull == 1:  # 긍부정 생성 안된것만
        statement = statement.where(and_(Saying.contents_good=="", Saying.contents_bad==""))
    elif isnull == 0:  # 긍정 or 부정 생성 된것만
        statement = statement.where(or_(Saying.contents_good!="", Saying.contents_bad!=""))

    if categories:  # 카테고리 필터링 됐다면,
        conditions = [Saying.category==cat for cat in categories]
        statement = statement.where(or_(*conditions))

    if keyword:  # 검색어 필터링 됐다면,
        statement = statement.where(or_(
            Saying.contents_kr.like(f"%{keyword}%"),
            Saying.contents_eng.like(f"%{keyword}%"),
            Saying.contents_good.like(f"%{keyword}%"),
            Saying.contents_bad.like(f"%{keyword}%")
        ))

    if consonants:  # 알파벳 필터링 됐다면,
        conditions = [Saying.contents_eng.ilike(f"{consonant}%") for consonant in consonants]
        statement = statement.where(or_(*conditions))

    # 토탈 페이지 확인
    total_record = session.exec(select(func.count()).select_from(statement)).one()
    total_page = (total_record // size) + bool(total_record % size)
    if p > total_page:
        p = total_page
    
    # 페이징 처리
    statement = paging(page=p, size=size, Table=Saying, statement=statement)  # tools/pagination.py 페이지 처리 툴
    filtered_sayings = session.exec(statement).all()
    
    return {
        "total_rows": total_record,
        "total_page": total_page,
        "content": filtered_sayings
    }


@saying_router.get("/create/")
async def create_texts(ids: List[int]=Query(...), session=Depends(get_session)):  # 긍부정 텍스트 생성
    
    start_time = datetime.now()  # 함수 실행시간 측정 시작

    for id in ids:
        saying = session.get(Saying, id)
        if saying:
            good_text, bad_text = await create_good_bad(meaning=saying.contents_detail)
            saying.contents_good = good_text
            saying.contents_bad = bad_text
            session.add(saying)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 id를 찾을 수 없습니다."
            )
    session.commit()

    end_time = datetime.now()  # 함수 실행시간 측정 종료
    execution_time = end_time - start_time

    return {"message": "긍부정 텍스트 생성 완료.", "함수 실행시간": execution_time}