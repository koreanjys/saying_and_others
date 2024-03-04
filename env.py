from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
END_POINT = os.getenv("END_POINT")

DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")
UVICORN_IP = os.getenv("UVICORN_IP")
UVICORN_PORT = os.getenv("UVICORN_PORT")
"""
main.py가 있는 디렉터리에 .env 파일을 생성하고 작성해야 한다.

-------작성 예제-------
API_KEY="***-*****"
END_POINT="https://pixabay.com/api/"

DATABASE_CONNECTION_STRING="mysql+pymysql://user:password@127.0.0.1:3306/db_name"
UVICORN_IP="0.0.0.0"
UVICORN_PORT=8000
-----------------------
"""