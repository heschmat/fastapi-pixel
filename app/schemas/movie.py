from pydantic import BaseModel, Field

class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    review: str = Field(..., min_length=1)
