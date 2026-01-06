from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Float,
    CheckConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as PgEnum

from app.core.base import Base
from app.models.enums import GenreEnum


class Movie(Base):
    __tablename__ = "movies"

    __table_args__ = (
        CheckConstraint(
            "release_year >= 1888",
            name="check_movie_release_year_min",
        ),
        CheckConstraint(
            "runtime > 0",
            name="check_movie_runtime_positive",
        ),
        CheckConstraint(
            "rating > 0 AND rating <= 10",
            name="check_movie_rating_range",
        ),
        CheckConstraint(
            "array_length(genres, 1) BETWEEN 1 AND 4",
            name="check_movie_genres_count",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )

    release_year: Mapped[int | None] = mapped_column(
        Integer,
        index=True,
        nullable=True,
    )

    runtime: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Runtime in minutes",
    )

    rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Rating from 0 to 10",
    )

    genres: Mapped[list[GenreEnum]] = mapped_column(
        ARRAY(
            PgEnum(
                GenreEnum,
                name="genre_enum",
                create_constraint=True,
            )
        ),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"<Movie id={self.id} "
            f"title={self.title} "
            f"year={self.release_year} "
            f"rating={self.rating}>"
        )
