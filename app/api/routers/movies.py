import logging
from fastapi import APIRouter, status

from app.schemas.movie import MovieCreate

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

@router.post("", status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate):
    logger.info("movie review received: title=%s", movie.title)
    return movie
