from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.review import ReviewCreate, ReviewOut
from app.core.database import get_db
from app.core.auth import get_current_user_from_token
from app.models.user import User
from app.services import review_service

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.post(
    "/movies/{movie_id}",
    response_model=ReviewOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    movie_id: int,
    review_in: ReviewCreate,
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    return await review_service.create_movie_review(
        db,
        movie_id=movie_id,
        user_id=current_user.id,
        content=review_in.content,
    )


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    await review_service.delete_movie_review(
        db,
        review_id=review_id,
        current_user_id=current_user.id,
    )
