from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MovieImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kind: str
    caption: str | None
    content_type: str
    file_size: int
    image_url: str
    created_at: datetime
