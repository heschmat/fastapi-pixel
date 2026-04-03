from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.movie import Movie
from app.schemas.movie import MovieCreate
from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.movie_repository import MovieRepository
from app.core.logging_utils import get_logger
from app.core.db_errors import commit_or_translate
from app.models.movie_image import MovieImage
from app.repositories.movie_image_repository import MovieImageRepository
from app.services.storage_service import (
    build_movie_image_object_key,
    upload_movie_image_bytes,
    get_presigned_download_url,
)

logger = get_logger(__name__)

repo = MovieRepository()
image_repo = MovieImageRepository()


async def create_movie(
    db: AsyncSession,
    *,
    movie_in: MovieCreate,
) -> Movie:
    # domain validation example
    if movie_in.release_year and movie_in.release_year > 2100:
        raise ValidationError("release_year is unrealistically high")

    movie = Movie(**movie_in.model_dump())
    repo.create(db, movie)
    await commit_or_translate(db)
    await db.refresh(movie)
    logger.info(
        "Movie created",
        extra={"movie_id": movie.id, "title": movie.title},
    )

    return movie


async def get_movie(db: AsyncSession, *, movie_id: int,) -> Movie | None:
    movie = await repo.get_by_id(db, movie_id)

    if not movie:
        raise NotFoundError(f"movie with id={movie_id} not found")

    return movie


async def get_movie_with_reviews(db: AsyncSession, *, movie_id: int,) -> Movie:
    movie = await repo.get_by_id(db, movie_id, with_reviews=True,)

    if not movie:
        raise NotFoundError(f"movie with id={movie_id} not found")
    
    for image in movie.images:
        image.image_url = get_presigned_download_url(image.object_key)

    return movie


async def list_movies(db: AsyncSession) -> list[Movie]:
    result = await db.execute(select(Movie))
    movies = result.scalars().all()
    logger.info("Fetched movie list", extra={"count": len(movies)})
    return movies


async def upload_movie_image(
    db: AsyncSession,
    *,
    movie_id: int,
    uploaded_by_user_id: int,
    file: UploadFile,
    kind: str,
    caption: str | None = None,
) -> MovieImage:
    movie = await repo.get_by_id(db, movie_id)
    if not movie:
        raise NotFoundError("Movie not found")

    if not file.content_type:
        raise ValidationError("File content type is required")

    data = await file.read()

    object_key = build_movie_image_object_key(
        movie_id=movie_id,
        uploaded_by_user_id=uploaded_by_user_id,
        content_type=file.content_type,
    )

    upload_movie_image_bytes(
        data=data,
        object_key=object_key,
        content_type=file.content_type,
    )

    image = MovieImage(
        movie_id=movie_id,
        uploaded_by_user_id=uploaded_by_user_id,
        object_key=object_key,
        content_type=file.content_type,
        file_size=len(data),
        kind=kind,
        caption=caption,
    )

    image_repo.create(db, image)
    await commit_or_translate(db)
    await db.refresh(image)

    image.image_url = get_presigned_download_url(image.object_key)
    return image
