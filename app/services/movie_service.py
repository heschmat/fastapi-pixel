from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.movie import Movie
from app.schemas.movie import MovieCreate
from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.movie_repository import MovieRepository
from app.core.logging_utils import get_logger

logger = get_logger(__name__)

repo = MovieRepository()


async def create_movie(
    db: AsyncSession,
    *,
    movie_in: MovieCreate,
) -> Movie:
    # domain validation example
    if movie_in.release_year and movie_in.release_year > 2100:
        raise ValidationError("release_year is unrealistically high")

    movie = Movie(**movie_in.model_dump())
    repo.add(db, movie)
    await db.commit()
    await db.refresh(movie)
    logger.info(
        "Movie created",
        extra={"movie_id": movie.id, "title": movie.title},
    )

    return movie


async def get_movie(db: AsyncSession, *, movie_id: int,) -> Movie | None:
    movie = await repo.get_by_id(db, movie_id)

    if not movie:
        raise NotFoundError(f"movie with id={movie_id} not found")

    return movie


async def get_movie_with_reviews(db: AsyncSession, *, movie_id: int,) -> Movie:
    movie = await repo.get_by_id(db, movie_id, with_reviews=True,)

    if not movie:
        raise NotFoundError(f"movie with id={movie_id} not found")

    return movie


async def list_movies(db: AsyncSession) -> list[Movie]:
    result = await db.execute(select(Movie))
    movies = result.scalars().all()
    logger.info("Fetched movie list", extra={"count": len(movies)})
    return movies
