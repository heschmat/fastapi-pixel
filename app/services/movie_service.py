from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.movie import Movie
from app.core.exceptions import NotFoundError, ValidationError
from app.core.logging_utils import get_logger

logger = get_logger(__name__)


async def create_movie(
    db: AsyncSession,
    *,
    title: str,
) -> Movie:
    if len(title) < 3:
        raise ValidationError("title too short")
    movie = Movie(title=title)
    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie


async def get_movie(db: AsyncSession, *, movie_id: int) -> Movie | None:
    result = await db.execute(
        select(Movie)
        .where(Movie.id == movie_id)
        .options(selectinload(Movie.reviews))
    )

    movie = result.scalar_one_or_none()

    if movie is None:
        raise NotFoundError(f"movie with id={movie_id} not found")
    
    return movie


async def list_movies(db: AsyncSession) -> list[Movie]:
    result = await db.execute(select(Movie))
    movies = result.scalars().all()
    logger.info("Fetched movie list", extra={"count": len(movies)})
    return movies
