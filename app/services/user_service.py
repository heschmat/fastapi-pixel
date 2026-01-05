from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.exceptions import NotFoundError, ValidationError


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
    
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        )


async def authenticate_user(
    db: AsyncSession,
    *,
    email: str,
    password: str,
) -> User | None:
    try:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )

    if not user or not verify_password(password, user.password_hash):
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        raise ValidationError(f"invalid credentials")

    return user
