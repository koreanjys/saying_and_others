import os  # os 모듈 import
from openai import OpenAI  # openai 모듈에서 OpenAI 클래스 import

OPENAI_API_KEY = OPENAI_API_KEY  # 사용자의 OpenAI API 키를 설정. 실제 사용자의 키로 대체해야 함
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY  # 환경변수에 API 키 설정

client = OpenAI(api_key=OPENAI_API_KEY)  # OpenAI 클라이언트 생성

with open("prompt.txt", "r") as file:  # 'prompt.txt' 파일을 읽기 모드('r')로 열기
    for line in file:  # 파일의 각 줄을 순차적으로 읽음
        korean_sentence = line.strip()  # 읽은 줄의 양쪽 끝에 있는 공백이나 개행문자를 제거하고 그 결과를 korean_sentence 변수에 저장

        # ChatGPT를 사용한 텍스트 번역 요청
        response_translation = client.chat_completions.create(
            model="gpt-3.5-turbo",  # 사용할 모델 지정
            messages=[{"role": "user", "content": f"Translate the following Korean text to English: '{korean_sentence}'"}]  # 번역 요청 메시지 설정
        )
        translated_sentence = response_translation.choices[0].message.content  # 번역된 문장 가져오기

        # DALL-E를 사용한 이미지 생성 요청
        response_image = client.images.generate(
            model="dall-e-3",  # 사용할 모델 지정
            prompt=translated_sentence,  # 이미지 생성 요청 시 사용할 프롬프트(번역된 영어 문장)
            size="1024x1024",  # 이미지 크기 지정
            quality="hd",  # 이미지 품질 지정
            n=1,  # 생성할 이미지의 개수 지정
        )

        image_url = response_image.data[0].url  # 생성된 이미지의 URL 가져오기
        print(image_url)  # 이미지 URL 출력
