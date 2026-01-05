from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="reviews")
    movie: Mapped["Movie"] = relationship(back_populates="reviews")

    def __repr__(self) -> str:
        return f"Review(id={self.id!r}, user_id={self.user_id!r}, movie_id={self.movie_id!r})"
