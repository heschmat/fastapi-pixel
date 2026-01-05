from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.review import Review
from app.models.movie import Movie
from app.core.exceptions import NotFoundError, ValidationError


async def create_review(
    db: AsyncSession,
    *,
    movie_id: int,
    user_id: int,
    content: str,
) -> Review:
    if len(content) < 5:
        raise ValidationError("review too short")

    movie = await db.get(Movie, movie_id)
    if not movie:
        raise NotFoundError("movie not found")

    review = Review(
        movie_id=movie_id,
        user_id=user_id,
        content=content,
    )

    db.add(review)
    await db.commit()
    await db.refresh(review)

    return review
