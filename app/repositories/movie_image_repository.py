from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie_image import MovieImage


class MovieImageRepository:
    def create(self, db: AsyncSession, image: MovieImage) -> None:
        db.add(image)
