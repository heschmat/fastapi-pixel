from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationError


def translate_integrity_error(exc: IntegrityError) -> Exception:
    """
    Translate SQLAlchemy IntegrityError into a domain-level exception.
    """

    # PostgreSQL constraint name (most reliable signal)
    constraint = getattr(exc.orig, "constraint_name", None)

    if constraint == "users_email_key":
        return ValidationError("Email already registered")

    if constraint == "uq_review_user_movie":
        return ValidationError("You have already reviewed this movie")

    # Fallback (safe default)
    return ValidationError("Invalid data")


async def commit_or_translate(db: AsyncSession):
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise translate_integrity_error(exc)
