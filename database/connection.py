# database/connection.py

from sqlmodel import SQLModel, Session, create_engine
import saying_env


def conn():
    SQLModel.metadata.create_all(engine_url)  # DB 연결 및 테이블 생성


# 세션을 관리하는 함수. FastAPI의 Depends()와 함께 사용하면 관리가 용이
def get_session():
    with Session(engine_url) as session:  # 세션을 종료하면 세션이 닫히도록 with문으로 작성
        yield session  # 각 작업마다 독립된 세션을 연결하기 위해 제너레이터 형태로 반환


engine_url = create_engine(url=saying_env.DATABASE_CONNECTION_STRING, echo=True)  # DB 엔진 생성