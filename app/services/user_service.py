# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from sqlalchemy.exc import SQLAlchemyError

# from fastapi import HTTPException, status

# from app.models.user import User
# from app.core.security import hash_password, verify_password
# from app.core.exceptions import NotFoundError, ValidationError, ServiceError, UnauthorizedError
# from app.core.logging_utils import get_logger

# logger = get_logger(__name__)

# async def register_user(db: AsyncSession, *, email: str, password: str) -> User:
#     user = User(
#         email=email,
#         password_hash=hash_password(password),
#     )

#     try:
#         # Check for existing user (HTTP concern)
#         result = await db.execute(
#             select(User).where(User.email == user.email)
#         )
#         if result.scalar_one_or_none():
#             # raise HTTPException(
#             #     status_code=400,
#             #     detail="Email already registered",
#             # )
#             raise ValidationError("Email already registered")

#         db.add(user)
#         await db.commit()
#         await db.refresh(user)

#         logger.info(
#             "User registered",
#             extra={"user_id": user.id, "email": email},
#         )

#         return user

#     except SQLAlchemyError as e:
#         await db.rollback()
#         raise ServiceError("Failed to create user") from e


# async def authenticate_user(
#     db: AsyncSession,
#     *,
#     email: str,
#     password: str,
# ) -> User | None:
#     try:
#         result = await db.execute(
#             select(User).where(User.email == email)
#         )

#         user = result.scalar_one_or_none()

#     except SQLAlchemyError as e: # Exception
#         # raise HTTPException(
#         #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         #     detail="Database error",
#         # )
#         raise ServiceError("Failed to authenticate user") from e

#     if not user or not verify_password(password, user.password_hash):
#         # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#         raise UnauthorizedError(f'invalid credentials')

#     return user

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.core.exceptions import NotFoundError, ValidationError
from app.core.security import hash_password


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

    try:
        await db.commit()
    except Exception:
        raise ValidationError("Email already in use")

    await db.refresh(user)
    return user
