from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.review import Review


class ReviewRepository:
    async def create(self, db: AsyncSession, review: Review) -> Review:
        db.add(review)

    async def get_by_id(
        self,
        db: AsyncSession,
        review_id: int,
    ) -> Review | None:
        result = await db.execute(
            select(Review).where(Review.id == review_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, db: AsyncSession, review: Review) -> None:
        await db.delete(review)
