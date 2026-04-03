from datetime import datetime
from pydantic import BaseModel


class MovieImageOut(BaseModel):
    id: int
    kind: str
    caption: str | None
    content_type: str
    file_size: int
    image_url: str
    created_at: datetime

    class Config:
        from_attributes = True
