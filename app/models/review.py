from datetime import datetime
from sqlalchemy import (
    Integer,
    ForeignKey,
    Text,
    DateTime,
    UniqueConstraint,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base


class Review(Base):
    __tablename__ = "reviews"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "movie_id",
            name="uq_review_user_movie",
        ),
        CheckConstraint(
            "length(content) > 0",
            name="check_review_content_not_empty",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="reviews",
        lazy="joined",
    )

    movie: Mapped["Movie"] = relationship(
        back_populates="reviews",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return (
            f"<Review id={self.id} "
            f"user_id={self.user_id} "
            f"movie_id={self.movie_id}>"
        )
