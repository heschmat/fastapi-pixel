from sqlalchemy.ext.asyncio import AsyncSession
from app.models.movie import Movie
from sqlalchemy import select


async def create_movie(
    db: AsyncSession,
    *,
    title: str,
    review: str,
) -> Movie:
    movie = Movie(
        title=title,
        review=review,
    )
    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie


async def get_movie(db: AsyncSession, movie_id: int) -> Movie | None:
    result = await db.execute(
        select(Movie).where(Movie.id == movie_id)
    )
    return result.scalar_one_or_none()
