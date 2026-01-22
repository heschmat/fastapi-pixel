"""
centralize all JWT parsing / verification in core/jwt.py.
Only jwt.py should know the exact encoding, decoding, expiration, etc.

=> the single source of truth for token creation and decoding
"""
from uuid import uuid4
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.core.config import settings
from app.core.exceptions import UnauthorizedError


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise UnauthorizedError("Invalid authentication token")

    sub = payload.get("sub")
    if sub is None:
        raise UnauthorizedError("Token missing subject")

    try:
        return int(sub)
    except ValueError:
        raise UnauthorizedError("Invalid token subject")

def create_refresh_token() -> str:
    # opaque token (not JWT)
    return uuid4().hex
