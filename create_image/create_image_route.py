# create_image/create_image_route.py

from fastapi import APIRouter, Query, File, UploadFile, Form, Body, Depends, status, HTTPException
from sqlmodel import select, func, join
from tools.pagination import paging
from database.connection import get_session
from typing import Optional
from openai import OpenAI
import saying_env

from pixabay.pixabay_model import PixabayCategory
from create_image.create_image_model import CreateImage, CreateImageForm

create_image_router = APIRouter(tags=["이미지 생성"])

# OpenAI 클라이언트 생성
client = OpenAI(api_key=saying_env.OPENAI_API_KEY)


# 프롬프트 받아서 이미지 생성하는 함수
def process_prompt(prompt: str, quantity: int):
    # DALL-E를 사용한 이미지 생성 요청
    response_image = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        n=quantity,
        response_format="b64_json"
    )
    return {"response": response_image, "data": response_image.data, "datum": response_image.data[0].b64_json}


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
        # images = session.exec(statement).all()  # 이건 왜 정의해놨지?
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
    category: str=Form(default=None)
    ):
    # if not category:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="카테고리를 입력해주세요."
    #     )
    # if quantity > 5:  # 수량 제한": quantity}
    #     quantity = 5

    if prompt:
        print(prompt, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        return {"result": prompt, "category": category, "quantity": quantity}
    else:
        if text_file is not None and text_file.content_type != "text/plain":
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="txt파일 형식이 아닙니다."
            )
        contents = await text_file.read()
        contents = contents.decode("utf-8")
        lines = contents.split("\r\n")
        print(lines, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        return {"result": lines, "category": category, "quantity": quantity}