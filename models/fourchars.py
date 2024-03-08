# models/fourchars.py

from typing import Optional
from sqlmodel import Field, SQLModel

from datetime import datetime, timedelta


# datetime의 출력 형태를 설정
def current_time_kst():
    return (datetime.utcnow() + timedelta(hours=9)).replace(microsecond=0)  # UTC + 9시간 = 한국 시간


class FourChar(SQLModel, table=True):  # 사자성어 테이블 모델 클래스

    # PK_ID
    id: Optional[int] = Field(default=None, primary_key=True)

    # 사용 필드
    contents_kr: str = Field(index=True, nullable=True)       # 사자성어(한글)*
    category: str = Field(index=True, nullable=True)          # 카테고리*
    contents_detail: str = Field(index=True, nullable=True)   # 뜻 풀이*
    contents_zh: Optional[str] = ""                           # 사자성어(한문)
    contents_good: str = ""
    contents_bad: str = ""

    # 자동생성 필드
    type_id: Optional[int] = 1
    use_yn: Optional[int] = 1
    created_at: datetime = Field(default_factory=current_time_kst, nullable=True)
    

    # 미사용 필드
    contents_divided: Optional[str] = ""
    url_name: Optional[str] = ""
    contents_eng: Optional[str] = ""
    author: Optional[str] = ""
    continent: Optional[str] = ""
    updated_at: Optional[datetime] = None


    #모델 설정
    model_config = {
        "json_schema_extra": {
            "example": {
                "category": "카테고리*",
                "contents_kr": "사자성어(한글)*",
                "contents_zh": "사자성어(한문)",
                "contents_detail": "뜻 풀이*"
            }
        }
    }


class FourCharUpdate(SQLModel):  # 사자성어 수정 모델 클래스
    url_name: Optional[str] = None
    contents_kr: Optional[str] = None
    contents_detail: Optional[str] = None
    type_id: Optional[int] = None
    category: Optional[str] = None
    contents_eng: Optional[str] = None
    contents_zh: Optional[str] = None
    contents_divided: Optional[str] = None
    author: Optional[str] = None
    continent: Optional[str] = None
    use_yn: Optional[int] = None
    contents_good: Optional[str] = None  # 긍정
    contents_bad: Optional[str] = None  # 부정

    # 모델 설정
    model_config = {
        "json_schema_extra": {
            "example": {
                "url_name": "출처(URL 혹은 블로그명)",
                "contents_kr": "사자성어 원본을 한국어로 작성",
                "contents_detail": "사자성어 원본을 해석",
                "type_id": "0: 명언  1: 사자성어",
                "category": "사자성어 분류(예시: 인생)",
                "contents_eng": "사자성어 원본을 영어로 작성",
                "contents_zh": "사자성어 원본을 한자로 작성",
                "contents_divided": "사자성어 해석을 한글로만 작성(특수문자 외국어 제거)",
                "author": "저자",
                "continent": "출처(지역)",
                "use_yn": "운영에 반영 여부 1: Yes  0: No"
            }
        }
    }