import logging
from fastapi import APIRouter, status, HTTPException

from app.schemas.movie import MovieCreate, MovieRead

from app.repositories.movies import MovieRepository

from app.core.exceptions import NotFoundError

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

repo = MovieRepository()

@router.post("", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate):
    created = repo.create(movie)
    logger.info("movie created: id=%s title=%s", created.id, created.title)
    return created

# @router.get("/{movie_id}", response_model=MovieRead)
# def get_movie(movie_id: int):
#     try:
#         movie_fetched = repo.get_by_id(movie_id)
#         logger.info("movie fetched: id=%s title=%s", movie_id, movie_fetched.title)
#         return movie_fetched
#     except NotFoundError as e:
#         raise HTTPException(status_code=404, detail=e.message)

@router.get("/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: int):
    movie_fetched = repo.get_by_id(movie_id)
    logger.info("movie fetched: id=%s title=%s", movie_id, movie_fetched.title)
    return movie_fetched


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