from typing import List, Optional

from app.schemas.movie import MovieCreate, MovieRead

from app.core.exceptions import NotFoundError, ValidationError


class MovieRepository:
    def __init__(self):
        self._movies: List[MovieRead] = []
        self._next_id = 1

    def create(self, movie: MovieCreate) -> MovieRead:
        if len(movie.title) < 3:
            raise ValidationError("title too short")
        
        movie_read = MovieRead(
            id=self._next_id,
            title=movie.title,
            review=movie.review,
        )
        self._movies.append(movie_read)
        self._next_id += 1
        return movie_read

    def list(self) -> List[MovieRead]:
        return self._movies

    def get_by_id(self, movie_id: int) -> Optional[MovieRead]:
        # return next((m for m in self._movies if m.id == movie_id), None)
        for movie in self._movies:
            if movie.id == movie_id:
                return movie
        raise NotFoundError(f"movie with id={movie_id} not found")
