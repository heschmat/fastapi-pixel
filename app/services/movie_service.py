from sqlalchemy.ext.asyncio import AsyncSession
from app.models.movie import Movie
from sqlalchemy import select

from app.core.exceptions import NotFoundError, ValidationError

async def create_movie(
    db: AsyncSession,
    *,
    title: str,
) -> Movie:
    if len(title) < 3:
        raise ValidationError("title too short")
    movie = Movie(
        title=title,
        review=review,
    )
    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie


async def get_movie(db: AsyncSession, *, movie_id: int) -> Movie | None:
    result = await db.execute(
        select(Movie).where(Movie.id == movie_id)
    )

    movie = result.scalar_one_or_none()

    if movie is None:
        raise NotFoundError(f"movie with id={movie_id} not found")
    
    return movie
