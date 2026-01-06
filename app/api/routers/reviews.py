from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.review import Review
from app.models.movie import Movie
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewOut
from app.services import review_service

router = APIRouter(
    prefix="",
    tags=["reviews"],
)


@router.post(
    "/movies/{movie_id}/reviews",
    response_model=ReviewOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    movie_id: int,
    payload: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # # ensure movie exists
    # result = await db.execute(
    #     select(Movie).where(Movie.id == movie_id)
    # )
    # movie = result.scalar_one_or_none()

    # if not movie:
    #     raise HTTPException(status_code=404, detail="Movie not found")

    review = await review_service.create_review(
        db,
        content=payload.content,
        user_id=current_user.id,
        movie_id=movie_id,
    )

    return review


# @router.delete(
#     "/reviews/{review_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_review(
#     review_id: int,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     result = await db.execute(
#         select(Review).where(Review.id == review_id)
#     )
#     review = result.scalar_one_or_none()

#     if not review:
#         raise HTTPException(status_code=404, detail="Review not found")

#     # ownership check
#     if review.user_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not allowed to delete this review",
#         )

#     await db.delete(review)
#     await db.commit()

@router.delete("/reviews/{review_id}",status_code=status.HTTP_204_NO_CONTENT,)
async def delete_review_endpoint(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await review_service.delete_review(
        db,
        review_id=review_id,
        user_id=current_user.id,
    )
