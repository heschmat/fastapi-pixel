import logging
from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.movie import MovieCreate, MovieOut
# from app.repositories.movies import MovieRepository
from app.services import movie_service
from app.core.exceptions import NotFoundError
from app.core.database import get_db
from app.core.logging_utils import get_logger

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

# repo = MovieRepository()

# @router.post("", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
# def create_movie(movie: MovieCreate):
#     created = repo.create(movie)
#     logger.info("movie created: id=%s title=%s", created.id, created.title)
#     return created

@router.post(
    "/",
    response_model=MovieOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_movie(
    movie: MovieCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    logger = get_logger(__name__, request)
    logger.info(
        "Creating movie",
        extra={
            "title": movie.title,
        },
    )

    created = await movie_service.create_movie(
        db,
        title=movie.title,
        review=movie.review,
    )

    logger.info("Movie created", extra={"movie_id": created.id},)

    return created


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
    response_model=MovieOut,
    status_code=status.HTTP_200_OK,
)
async def get_movie(
    movie_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    logger = get_logger(__name__, request)

    logger.info(
        "Fetching movie",
        extra={
            "movie_id": movie_id,
        },
    )

    movie = await movie_service.get_movie(db, movie_id=movie_id)

    # if not movie:
    #     logger.warning(
    #         "Movie not found",
    #         extra={"movie_id": movie_id},
    #     )
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Movie not found",
    #     )

    logger.info(
        "Movie fetched successfully",
        extra={"movie_id": movie.id},
    )

    return movie
