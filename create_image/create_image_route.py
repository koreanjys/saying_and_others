# create_image/create_image_route.py

from fastapi import APIRouter, Query, File, UploadFile, Form, Body, Depends, status, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import select, func, join, delete
from tools.pagination import paging
from tools.create_image import process_prompt
from database.connection import get_session
from typing import Optional, List

from pixabay.pixabay_model import PixabayCategory
from create_image.create_image_model import CreateImage

from datetime import datetime

create_image_router = APIRouter(tags=["이미지 생성"])


@create_image_router.get("/")
async def retrieve_all_created_images(
    p: int=Query(default=1),
    size: int=Query(default=12),
    keyword: str=Query(default=None),
    category: str=Query(default=None),
    session=Depends(get_session)
    ):
    statement = select(CreateImage)

    if keyword:
        statement = statement.where(CreateImage.prompt.like(f"%{keyword}%"))
    if category:
        statement = statement.join(PixabayCategory).where(PixabayCategory.category==category)

    # 토탈 페이지 확인
    total_record = session.exec(select(func.count()).select_from(statement)).one()
    total_page = (total_record // size) + bool(total_record % size)
    if p > total_page:
        p = total_page
    
    # 페이징 처리
    statement = paging(page=p, size=size, Table=CreateImage, statement=statement)
    contents = session.exec(statement).all()

    return {
        "total_rows": total_record,
        "total_page": total_page,
        "contents": contents
    }


@create_image_router.get("/{id}", response_model=CreateImage)
async def retrieve_created_image(id: int, session=Depends(get_session)) -> CreateImage:
    created_image = session.get(CreateImage, id)
    if created_image:
        return created_image
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 데이터가 존재하지 않습니다."
    )


@create_image_router.post("/")
async def create_image(
    prompt: str=Form(default=None),
    text_file: UploadFile=File(default=None),
    quantity: int=Form(default=1),
    category: str=Form(default=None),
    session=Depends(get_session)
    ):

    start_time = datetime.now()  # 함수 시간 측정 (시작 시간)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="카테고리를 입력해주세요."
        )
    # 카테고리 인스턴스 불러오기
    statement = select(PixabayCategory).where(PixabayCategory.category==category)
    try:
        category_instance = session.exec(statement).one()
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 카테고리 입니다."
        )
    if quantity != 1:  # 현재 dall-e-3 모델은 quantity 파라미터가 1만 받아짐
        quantity = 1

    if prompt:
        created_url = await process_prompt(prompt=prompt, quantity=quantity)
        created_image = CreateImage(created_url=created_url, prompt=prompt, pixabay_category=category_instance, isnew=1)
        session.add(created_image)
        session.commit()
        
        end_time = datetime.now()  # 함수 시간 측정 (종료 시간)
        execution_time = end_time - start_time

        return {"message": "이미지 생성이 완료되었습니다.", "실행 시간": execution_time}
    else:
        if text_file is not None and text_file.content_type != "text/plain":
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="txt파일 형식이 아닙니다."
            )
        contents = await text_file.read()
        contents = contents.decode("utf-8")
        lines = contents.split("\r\n")
        return {"result": lines, "category": category, "quantity": quantity}


@create_image_router.delete("/delete/")
async def delete_created_images(ids: List[int]=Query(...), session=Depends(get_session)):
    for id in ids:
        created_image = session.get(CreateImage, id)
        if created_image:
            session.delete(created_image)
            session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="선택한 id가 존재하지 않습니다."
            )
    return {
        "message": "삭제를 완료했습니다."
    }