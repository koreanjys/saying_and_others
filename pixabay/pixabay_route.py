from fastapi import APIRouter, Query, Depends, status, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import select, func, or_, join, delete
from database.connection import get_session
from tools.pagination import paging
from tools.pixabay_image import run_urls_to_images

import requests
import saying_env
from typing import List

from pixabay.pixabay_model import PixabayData, PixabayCategory
from create_image.create_image_model import CreateImage

import base64
import time
"""
model을 불러올 때, 필요한 model 뿐만 아니라 Relationships 으로 연결된 모든 모델을 불러와야 하기 때문에
그 부분을 추후에 신경써서 설계를 하도록 하자.
"""

pixabay_router = APIRouter(tags=["이미지 데이터 스크래핑"])


# 이미지 카테고리 GET
@pixabay_router.get("/image_categories/", response_model=List[PixabayCategory])
async def retrieve_image_categories(session=Depends(get_session)) -> List[PixabayCategory]:
    statement = select(PixabayCategory).order_by(PixabayCategory.id)
    categories = session.exec(statement).all()
    return categories


@pixabay_router.get("/")
async def retrieve_all_data(keyword: str=Query(default=None),
                            category: str=Query(default=None),
                            p: int=Query(default=1),
                            size: int=Query(default=12),
                            crawling_on: int=Query(default=0),
                            session=Depends(get_session)):
    """
    쿼리 crawling_on=1 은 크롤링을 하고, 데이터베이스에 저장하는 프로세스를 진행함. 그 다음 데이터베이스에서 키워드와 카테고리가 일치하는 데이터를 불러옴\n
    쿼리 crawling_on=0 은 크롤링을 하지 않고, 데이터베이스에서 키워드와 카테고리가 일치하는 데이터를 불러옴
    """
    if crawling_on == 1:
        if not category:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="카테고리를 선택하지 않았습니다."
            )
        category_instance = session.exec(select(PixabayCategory).where(PixabayCategory.category==category)).one()

        q = keyword
        per_page: int = 200

        params = {
            "q": q,
            "per_page": per_page,
            "key": saying_env.API_KEY,
            "lang": "ko",
            "safesearch": "true"
        }   
        get_api = requests.get(url=saying_env.END_POINT, params=params)
        try:
            image_data = get_api.json()["hits"]
            image_urls = [datum["webformatURL"] for datum in image_data]
            images = await run_urls_to_images(image_urls)
            for datum, image in zip(image_data, images):
                pixabay_instance = PixabayData(
                    image_id=datum["id"],
                    imageURL=image,
                    tags=datum["tags"],
                    user=datum["user"],
                    type=datum["type"],
                    imageWidth=datum["webformatWidth"],
                    imageHeight=datum["webformatHeight"],
                    keyword=q,
                    isnew=1,
                    pixabay_category=category_instance
                )
                isexist = session.exec(select(PixabayData).where(PixabayData.image_id==pixabay_instance.image_id)).first()
                if isexist:  # image_id가 이미 존재하면 add 하지 않음
                    isexist.isnew = 0
                    session.add(isexist)
                    session.commit()
                    continue
                session.add(pixabay_instance)
            session.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"API에서 해당 데이터를 가져올 수 없습니다.{e}"
            )
    
    statement = select(PixabayData)

    if keyword:
        statement = statement.where(PixabayData.keyword.like(f"%{keyword}%"))
    if category:
        statement = statement.join(PixabayCategory).where(PixabayCategory.category==category)

    total_record = session.exec(select(func.count()).select_from(statement)).one()
    total_page = (total_record // size) + bool(total_record % size)
    if p > total_page:
        p = total_page

    statement = paging(page=p, size=size, Table=PixabayData, statement=statement)
    image_data = session.exec(statement).all()

    return {
        "total_page": total_page,
        "total_record": total_record,
        "contents": image_data
    }


@pixabay_router.get("/{id}")
async def retrieve_data(id: int, session=Depends(get_session)):
    datum = session.get(PixabayData, id)
    if not datum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 id를 찾을 수 없습니다."
        )
    res = requests.get(datum.imageURL)
    image_data = res.content
    base64_encoded = base64.b64encode(image_data).decode('utf-8')  # 바이너리 데이터를 base64로 인코딩
    return {"data": datum, "binary": base64_encoded, "length": len(base64_encoded)}


@pixabay_router.get("/download/")
async def download_crawling_images(ids: List[int]=Query(...), session=Depends(get_session)):
    for id in ids:
        statement = select(PixabayData).where(PixabayData.image_id==id)
        # pixabay_data = 


@pixabay_router.delete("/delete/")
async def delete_crawling_data(ids: List[int]=Query(...), session=Depends(get_session)):
    for id in ids:
        statement = select(PixabayData).where(PixabayData.image_id==id)
        pixabay_data = session.exec(statement).first()
        if pixabay_data:
            session.delete(pixabay_data)
            session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"선택한 id : {id} 를 찾을 수 없습니다."
            )
    return {"message": "삭제를 완료 했습니다."}