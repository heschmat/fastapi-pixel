from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.movie import Movie


class MovieRepository:
    async def create(self, db: AsyncSession, movie: Movie) -> Movie:
        db.add(movie)

    async def get_by_id(
        self,
        db: AsyncSession,
        movie_id: int,
        *,
        with_reviews: bool = False,
    ) -> Movie | None:
        stmt = select(Movie).where(Movie.id == movie_id)
        if with_reviews:
            stmt = stmt.options(selectinload(Movie.reviews))
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
