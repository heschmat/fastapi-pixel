""" just orchestrates user retrieval using the public API of core/jwt.py"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.core.exceptions import UnauthorizedError
from app.core.jwt import decode_access_token
from app.repositories.user_repository import UserRepository


repo = UserRepository()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    user_id = decode_access_token(token)
    user = await repo.get_by_id(db, user_id)

    if not user:
        raise UnauthorizedError("User not found")

    return user
