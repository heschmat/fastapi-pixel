import logging
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    File,
    Form,
    UploadFile,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.movie import MovieCreate, MovieOut, MovieDetailOut
from app.schemas.movie_image import MovieImageOut
from app.services import movie_service
from app.core.database import get_db
from app.core.logging_utils import get_logger
from app.core.auth import get_current_user_from_token
from app.models.user import User


router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

logger = get_logger(__name__)

# repo = MovieRepository()

# @router.post("", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
# def create_movie(movie: MovieCreate):
#     created = repo.create(movie)
#     logger.info("movie created: id=%s title=%s", created.id, created.title)
#     return created

@router.post(
    "",
    response_model=MovieOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_movie(
    movie_in: MovieCreate,
    request: Request,
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    # logger = get_logger(__name__, request)
    logger.info("Creating movie", extra={"title": movie_in.title, "user_id": current_user.id})
    movie = await movie_service.create_movie(
        db,
        movie_in=movie_in,
        # created_by=current_user,
    )
    return movie


# @router.get("/{movie_id}", response_model=MovieRead)
# def get_movie(movie_id: int):
#     try:
#         movie_fetched = repo.get_by_id(movie_id)
#         logger.info("movie fetched: id=%s title=%s", movie_id, movie_fetched.title)
#         return movie_fetched
#     except NotFoundError as e:
#         raise HTTPException(status_code=404, detail=e.message)

# @router.get("/{movie_id}", response_model=MovieRead)
# def get_movie(movie_id: int):
#     # movie_fetched = repo.get_by_id(movie_id)
#     movie_fetched = movie_service.get_movie(movie_id)
#     logger.info("movie fetched: id=%s title=%s", movie_id, movie_fetched.title)
#     return movie_fetched


"""
# if in get_movie() you simply do `return` instead of `return movie_fetched`:

Your route declares response_model=MovieRead
But the function returns None
FastAPI then tries to serialize None into MovieRead

That causes:
ResponseValidationError:
Input should be a valid dictionary or object to extract fields from
input: None

"""

@router.get(
    "/{movie_id}",
    response_model=MovieDetailOut,
    status_code=status.HTTP_200_OK,
)
async def get_movie_detail(
    movie_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    # logger.info("Fetching movie",extra={"movie_id": movie_id,},)

    # movie = await movie_service.get_movie(db, movie_id=movie_id)

    # logger.info("Movie fetched successfully",extra={"movie_id": movie.id},)

    # return movie
    return await movie_service.get_movie_with_reviews(
        db,
        movie_id=movie_id,
    )


@router.get("", response_model=list[MovieOut])
async def get_movies(db: AsyncSession = Depends(get_db)):
    # optional intent logging
    logger.info("Request received: list movies")
    return await movie_service.list_movies(db)


@router.post(
    "/{movie_id}/images",
    response_model=MovieImageOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_movie_image(
    movie_id: int,
    file: UploadFile = File(...),
    kind: str = Form(...),
    caption: str | None = Form(None),
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    data = await file.read()

    return await movie_service.upload_movie_image(
        db,
        movie_id=movie_id,
        uploaded_by_user_id=current_user.id,
        data=data,
        content_type=file.content_type or "",
        kind=kind,
        caption=caption,
    )
