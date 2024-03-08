# tools/create_good_bad.py

from openai import OpenAI
import saying_env

# 클라이언트 생성
client = OpenAI(api_key=saying_env.OPENAI_API_KEY)


# 주어진 사자성어를 ChatGPT에게 긍정적인 해석과 부정적인 해석을 물어보는 함수
async def create_good_bad(meaning, to_good_prompt=None, to_bad_prompt=None):
    if not to_good_prompt:
        to_good_prompt = "이 문장을 긍정적인 관점에서 해석하고 위로의 말을 만들어주세요. 원래 뜻에서 벗어나지 않도록 만들어주세요."
    if not to_bad_prompt:
        to_bad_prompt = "이 문장을 부정적인 관점에서 해석하고 경고의 말을 만들어주세요. 원래 뜻에서 벗어나지 않도록 만들어주세요."
    
    # ChatGPT를 사용한 텍스트 분류 요청 (긍정적 해석)
    positive_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"'{meaning}'. {to_good_prompt}"}],
    )

    # ChatGPT를 사용한 텍스트 분류 요청 (부정적 해석)
    negative_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"'{meaning}'. {to_bad_prompt}"}],
    )

    # 응답에서 긍정적, 부정적 해석 추출
    positive_interpretation = positive_response.choices[0].message.content
    negative_interpretation = negative_response.choices[0].message.content

    return positive_interpretation, negative_interpretation