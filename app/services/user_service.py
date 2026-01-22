from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.core.exceptions import NotFoundError, ValidationError
from app.core.security import hash_password
from app.core.db_errors import commit_or_translate


repo = UserRepository()


async def get_user(
    db: AsyncSession,
    *,
    user_id: int,
):
    user = await repo.get_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")
    return user


async def update_user(
    db: AsyncSession,
    *,
    user_id: int,
    email: str | None = None,
    password: str | None = None,
):
    user = await repo.get_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")

    if email:
        user.email = email

    if password:
        user.password_hash = hash_password(password)

    await repo.update(db, user)
    await commit_or_translate(db)
    await db.refresh(user)
    return user
