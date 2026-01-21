from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User


class UserRepository:
    async def get_by_email(
        self,
        db: AsyncSession,
        email: str,
    ) -> User | None:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> User | None:
        return await db.get(User, user_id)

    async def create(
        self,
        db: AsyncSession,
        user: User,
    ) -> User:
        db.add(user)
        # ⚠️respository should not commit transactions; they should be handled at the service layer
        # ⚠️repository mutate the session but do not finalize changes
        # await db.commit()
        # await db.refresh(user)
        # return user
