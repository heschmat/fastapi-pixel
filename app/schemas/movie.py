from pydantic import BaseModel, Field
from typing import List
from app.schemas.review import ReviewOut

class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class MovieOut(BaseModel):
    id: int
    title: str
    # reviews: List[ReviewOut] = []

    class Config:
        from_attributes = True


class MovieDetailOut(MovieOut):
    reviews: List[ReviewOut]
