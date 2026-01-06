from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# from app.models.review import Review
# from app.models.movie import Movie
from app.models import Movie, Review
from app.core.exceptions import NotFoundError, ValidationError, ForbiddenError
from app.core.logging_utils import get_logger


logger = get_logger(__name__)

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

    logger.info(
        "Review created",
        extra={
            "review_id": review.id,
            "movie_id": movie_id,
            "user_id": user_id,
        },
    )

    return review


async def delete_review(
    db: AsyncSession,
    *,
    review_id: int,
    user_id: int,
) -> None:
    result = await db.execute(
        select(Review).where(Review.id == review_id)
    )
    review = result.scalar_one_or_none()

    if not review:
        raise NotFoundError("Review not found")

    if review.user_id != user_id:
        raise ForbiddenError("Not allowed to delete this review")

    await db.delete(review)
    await db.commit()

    logger.info(
        "Review deleted",
        extra={
            "review_id": review_id,
            "user_id": user_id,
        },
    )
