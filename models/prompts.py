# models/prompts.py

# 사용 여부는 미확정
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timedelta

# class Prompt(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     prompt: Optional[str] = None
#     created_at: Optional[datetime] = datetime.utcnow() + timedelta(hours=9)