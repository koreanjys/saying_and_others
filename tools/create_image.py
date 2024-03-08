# tools/create_image.py

from openai import OpenAI
import saying_env

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
        # response_format="b64_json"  # 이미지 URL 대신 base64 형태로 받아오기
    )
    return response_image.data[0].url