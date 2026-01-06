from typing import List, Optional
from pydantic import BaseModel, Field, conint, confloat
from app.models.enums import GenreEnum
from app.schemas.review import ReviewOut


class MovieCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)

    release_year: Optional[conint(ge=1888)] = None

    runtime: conint(gt=0)

    rating: Optional[confloat(gt=0, le=10)] = None

    genres: List[GenreEnum] = Field(
        min_length=1,
        max_length=4,
        description="List of 1 to 4 genres",
    )


class MovieOut(BaseModel):
    id: int
    title: str
    release_year: Optional[int]
    runtime: int
    rating: Optional[float]
    genres: List[GenreEnum]

    class Config:
        from_attributes = True


class MovieDetailOut(MovieOut):
    reviews: List[ReviewOut] = Field(default_factory=list)
