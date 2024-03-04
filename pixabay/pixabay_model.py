# pixabay/pixabay_model.py

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timedelta


class PixabayData(SQLModel, table=True):
    image_id: Optional[int] = Field(default=None, primary_key=True)
    type: Optional[str] = None
    tags: Optional[str] = None
    user: Optional[str] = None
    keyword: Optional[str] = Field(index=True)
    imageURL: Optional[str] = None
    created_at: Optional[datetime] = datetime.utcnow() + timedelta(hours=9)

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    pixabay_category: Optional["PixabayCategory"] = Relationship(back_populates="pixabay_data")



class PixabayCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: Optional[str] = None

    pixabay_data: List[PixabayData] = Relationship(back_populates="pixabay_category")
