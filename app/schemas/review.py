from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)

class ReviewOut(BaseModel):
    id: int
    content: str
    user_id: int

    class Config:
        from_attributes = True
