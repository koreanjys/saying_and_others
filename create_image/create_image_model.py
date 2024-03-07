# create_image/create_image_model.py

from fastapi import UploadFile
from sqlmodel import SQLModel, Field, Relationship, BLOB
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pixabay.pixabay_model import PixabayCategory


class CreateImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_url: Optional[str] = None
    prompt: Optional[str] = None
    category_id: Optional[int] = Field(default=None, foreign_key="pixabaycategory.id")

    pixabay_category: Optional["PixabayCategory"] = Relationship(back_populates="created_data")


class CreateImageForm(SQLModel):
    prompt: Optional[str] = None
    text_file: Optional[UploadFile] = None
    quantity: int = 1
    category: str