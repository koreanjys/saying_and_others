from fastapi import APIRouter, Query, Depends, status, HTTPException
from sqlmodel import select, func, or_
from database.connection import get_session
from tools.pagination import paging
import requests
import env

from pixabay.pixabay_model import PixabayData, PixabayCategory
from create_image.create_image_model import CreateImage
"""
model을 불러올 때, 필요한 model 뿐만 아니라 Relationships 으로 연결된 모든 모델을 불러와야 하기 때문에
그 부분을 추후에 신경써서 설계를 하도록 하자.
"""

pixabay_router = APIRouter(tags= ["이미지 크롤링"])


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
        q = keyword
        per_page: int = 200  

        statement = select(PixabayCategory).where(PixabayCategory.category==category)
        category_instance = session.exec(statement).first()

        if not category_instance:
            category_instance = PixabayCategory(category=category)

        params = {
            "q": q,
            "per_page": per_page,
            "key": env.API_KEY,
            "lang": "ko",
            "safesearch": "true"
        }   
        get_api = requests.get(url=env.END_POINT, params=params)
        try:
            image_data = get_api.json()["hits"]
            for datum in image_data:
                pixabay_instance = PixabayData(
                    id=datum["id"],
                    imageURL=datum["webformatURL"],
                    tags=datum["tags"],
                    user=datum["user"],
                    type=datum["type"],
                    keyword=q,
                    pixabay_category=category_instance
                )
                session.add(pixabay_instance)
                try:
                    session.commit()
                except:
                    session.rollback()
        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API에서 해당 데이터를 가져올 수 없습니다."
            )
    
    statement = select(PixabayData).where(PixabayData.keyword.like(f"%{keyword}%"))
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
