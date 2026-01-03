from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.base import Base

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    review: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self) -> str:
        return f"Movie(id={self.id!r}, title={self.title!r})"
    