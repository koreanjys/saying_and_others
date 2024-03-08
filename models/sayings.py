# models/sayings.py

from typing import Optional
from sqlmodel import Field, SQLModel

from datetime import datetime, timedelta


# datetime의 출력 형태를 설정
def current_time_kst():
    return (datetime.utcnow() + timedelta(hours=9)).replace(microsecond=0)  # UTC + 9시간 = 한국 시간


class Saying(SQLModel, table=True):  # 명언 테이블 모델 클래스

    # PK_ID
    id: Optional[int] = Field(default=None, primary_key=True)

    # 사용 필드
    category: str = Field(index=True, nullable=True)      # 카테고리*
    author: str = Field(index=True, nullable=True)        # 발화자*
    contents_kr: str = Field(index=True, nullable=True)   # 뜻 풀이*
    contents_eng: str = Field(index=True, default="", nullable=True)      # 영문 명언
    contents_good: str = ""
    contents_bad: str = ""

    # 자동생성 필드
    type_id: Optional[int] = 0
    use_yn: Optional[int] = 1
    created_at: datetime = Field(default_factory=current_time_kst, nullable=True)

    # 미사용 필드
    contents_detail: Optional[str] = ""
    url_name: Optional[str] = ""
    contents_zh: Optional[str] = ""
    contents_divided: Optional[str] = ""
    continent: Optional[str] = ""
    updated_at: Optional[datetime] = None

    #모델 설정
    model_config = {
        "json_schema_extra": {
            "example": {
                "category": "카테고리*",
                "author": "발화자*",
                "contents_kr": "뜻 풀이*",
                "contents_en": "영문 명언"
            }
        }
    }


class SayingUpdate(SQLModel):  # 명언 수정 모델 클래스
    contents_kr: Optional[str] = None   # 수정 필드
    category: Optional[str] = None      # 수정 필드
    contents_eng: Optional[str] = None  # 수정 필드
    author: Optional[str] = None        # 수정 필드
    url_name: Optional[str] = None
    contents_detail: Optional[str] = None
    type_id: Optional[int] = None
    contents_zh: Optional[str] = None
    contents_divided: Optional[str] = None
    continent: Optional[str] = None
    use_yn: Optional[int] = None
    contents_good: Optional[str] = None  # 긍정
    contents_bad: Optional[str] = None  # 부정

    # 모델 설정
    model_config = {
        "json_schema_extra": {
            "example": {
                "category": "명언 카테고리(예시: 인생)",
                "contents_eng": "영문 명언",
                "author": "명언 발화자",
                "contents_kr": "명언 뜻 풀이"
            }
        }
    }