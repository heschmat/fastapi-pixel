from datetime import datetime
from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    # content: str = Field(min_length=1)
    content: str = Field(..., min_length=1, max_length=5000)

class ReviewOut(BaseModel):
    id: int
    content: str
    user_id: int
    movie_id: int
    created_at: datetime

    class Config:
        from_attributes = True
