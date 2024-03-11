# tools/create_image.py

from openai import OpenAI
import saying_env

import base64
import io
import requests
from PIL import Image

# OpenAI 클라이언트 생성
client = OpenAI(api_key=saying_env.OPENAI_API_KEY)


def process_image_to_base64(url):  # openai API에서 이미지 url을 생성 후 jpeg로 변환
  response = requests.get(url)
  image_bytes = io.BytesIO(response.content)
  img = Image.open(image_bytes)
  jpeg_image = io.BytesIO()
  img.save(jpeg_image, format='JPEG')
  jpeg_image.seek(0)
  base64_string = base64.b64encode(jpeg_image.read()).decode('utf-8')
  return "data:image/jpeg;base64," + base64_string


# 프롬프트 받아서 이미지 생성하는 함수
async def process_prompt(prompt: str, quantity: int):
    # DALL-E를 사용한 이미지 생성 요청
    response_image = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        # quality="hd",  # dall-e-3 모델에만 적용
        n=quantity,
        # response_format="b64_json"  # 이미지 URL 대신 base64 형태로 받아오기(용량이 4mb라 url을 jpeg로 변환. 용량 약 200~300kb)
    )
    image = response_image.data[0]
    image.url = process_image_to_base64(image.url)
    return image.url