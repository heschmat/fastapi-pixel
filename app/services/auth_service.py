from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, hash_password
from app.core.jwt import create_access_token
from app.core.db_errors import commit_or_translate
from app.core.exceptions import ValidationError, UnauthorizedError
from app.core.logging_utils import get_logger
from app.repositories.user_repository import UserRepository

repo = UserRepository()

# logger = get_logger(__name__)
# repo = UserRepository()


# async def login(
#     db: AsyncSession,
#     *,
#     email: str,
#     password: str,
# ) -> str:
#     user = await repo.get_by_email(db, email)

#     if not user or not verify_password(password, user.password_hash):
#         raise UnauthorizedError("Invalid email or password")

#     token = create_access_token(user.id)

#     logger.info(
#         "User logged in",
#         extra={"user_id": user.id},
#     )

#     return token


async def register_user(
    db: AsyncSession,
    *,
    email: str,
    password: str,
) -> User:
    user = User(
        email=email,
        password_hash=hash_password(password),
    )

    # service layer should handle transaction finalization
    existing_user = await repo.get_by_email(db, email)
    if existing_user:
        raise ValidationError("Email already registered")

    await repo.create(db, user)
    await commit_or_translate(db)
    await db.refresh(user)
    return user


from app.core.jwt import (
    create_access_token,
    create_refresh_token,
)
from app.core.security import (
    hash_token,
    verify_token,
)
from app.core.exceptions import UnauthorizedError


async def authenticate_user(
    db: AsyncSession,
    *,
    email: str,
    password: str,
):
    user = await repo.get_by_email(db, email)

    if not user or not verify_password(password, user.password_hash):
        raise UnauthorizedError("Invalid email or password")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token()

    user.refresh_token_hash = hash_token(refresh_token)
    await db.commit()

    return access_token, refresh_token


async def rotate_refresh_token(
    db: AsyncSession,
    *,
    user_id: int,
    refresh_token: str,
) -> tuple[str, str]:
    user = await repo.get_by_id(db, user_id)

    if (
        not user
        or not user.refresh_token_hash
        or not verify_token(refresh_token, user.refresh_token_hash)
    ):
        raise UnauthorizedError("Invalid refresh token")

    new_access = create_access_token(user.id)
    new_refresh = create_refresh_token()

    user.refresh_token_hash = hash_token(new_refresh)
    await db.commit()

    return new_access, new_refresh
