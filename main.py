# main.py

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from contextlib import asynccontextmanager

from database.connection import conn

from routes.sayings import saying_router
from routes.fourchars import fourchar_router
from routes.category import category_router
from pixabay.pixabay_route import pixabay_router

from database.connection import settings

from starlette.middleware.cors import CORSMiddleware


# lifesapn : 어플리케이션 시작과 종료 시 실행되는 프로세스 작성
@asynccontextmanager
async def lifesapn(app: FastAPI):
    # 앱 시작 시 작동되는 코드 작성
    conn()  # DB 연결 및 초기화

    yield
    # 앱 종료 시 작동되는 코드 작성


app = FastAPI(lifespan=lifesapn)  # FastAPI 인스턴스 생성


# CORS 설정(허가할 origin 주소를 리스트에 추가)
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우트 등록
app.include_router(saying_router, prefix="/saying")  # 명언
app.include_router(fourchar_router, prefix="/fourchar")  # 사자성어
app.include_router(category_router, prefix="/category")  # 명언 카테고리
app.include_router(pixabay_router, prefix="/pixabay")  # 이미지 크롤링


# 첫 화면
@app.get("/")
async def main() -> dict:
    return {
        "message": "명언 조회 URL 입니다."
    }


# uvicorn 앱 실행
if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.UVICORN_IP, port=settings.UVICORN_PORT, reload=True)