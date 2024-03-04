# pixabay/pixabay_route.py

from fastapi import APIRouter, Path, Depends
from pixabay.pixabay_model import PixabayData, PixabayCategory
from sqlmodel import select
from database.connection import get_session


pixabay_router = APIRouter(tags= ["Pixabay"])


@pixabay_router.get("/")
async def retrieve_all_data(keyword: str=Path(default=None),
                             category: str=Path(default=None),
                               p: int=Path(default=1),
                                 crawling_on: int=Path(default=0),
                                 session=Depends(get_session)):
    
    if crawling_on == 1:  # 찾기 버튼을 클릭 했다면
        # 파라미터 입력
        q = keyword
        per_page: int = 200  # 3~200
        image_type: str = "photo"

        params = {
        "q": q,
        "per_page": per_page,
        "key": env.API_KEY,
        "lang": "ko",
        "category": category,
        "colors": colors,
        "order": order
                }   
        image_data = []  # ResponseData 모델의 인스턴스들을 받아올 리스트