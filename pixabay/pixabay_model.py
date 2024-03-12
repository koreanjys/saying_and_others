# pixabay/pixabay_model.py

from sqlmodel import SQLModel, Field, Relationship, Column, Text
from datetime import datetime, timedelta
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from create_image.create_image_model import CreateImage


class PixabayData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    image_id: int
    isnew: int
    type: Optional[str] = None
    tags: Optional[str] = None
    user: Optional[str] = None
    keyword: Optional[str] = Field(index=True)
    imageURL: str = Field(sa_column=Column(Text(length=300000)))  # URL이 매우 길다.
    imageWidth: Optional[int] = None
    imageHeight: Optional[int] = None
    created_at: Optional[datetime] = datetime.utcnow() + timedelta(hours=9)
    category_id: Optional[int] = Field(default=None, foreign_key="pixabaycategory.id")

    pixabay_category: Optional["PixabayCategory"] = Relationship(back_populates="pixabay_data")


class PixabayCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: Optional[str] = None

    pixabay_data: List[PixabayData] = Relationship(back_populates="pixabay_category")
    created_data: List["CreateImage"] = Relationship(back_populates="pixabay_category")