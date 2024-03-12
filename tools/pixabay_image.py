import aiohttp
import asyncio
import base64

async def url_to_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img_data = await response.read()  # 이미지 데이터를 비동기적으로 읽습니다.
            img_base64 = base64.b64encode(img_data).decode("utf-8")  # Base64로 인코딩합니다.
            return "data:image/jpg;base64," + img_base64

async def run_urls_to_images(urls: list):
    tasks = [url_to_image(url) for url in urls]  # 각 URL에 대한 비동기 작업을 생성합니다.
    converted_images = await asyncio.gather(*tasks)  # 모든 작업을 비동기적으로 실행합니다.
    return converted_images