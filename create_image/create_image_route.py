# create_image/create_image_route.py

from fastapi import APIRouter, Query, File, UploadFile, Form
from typing import Optional

create_image_router = APIRouter(tags=["이미지 생성"])


@create_image_router.get("/")
async def create_image_main(
    p: int=Query(default=1),
    size: int=Query(default=12),
    keyword: str=Query(default=None),
    category: str=Query(default=None)
    ):
    pass


@create_image_router.post("/")
async def create_image(
    prompt: str=Form(default=None),
    
    ):
    pass