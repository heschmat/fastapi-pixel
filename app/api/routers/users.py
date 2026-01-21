from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import get_current_user_from_token
from app.schemas.users import UserOut, UserUpdate
from app.models.user import User
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=UserOut)
async def get_me(
    current_user: User = Depends(get_current_user_from_token),
):
    return current_user


@router.put("/me", response_model=UserOut)
async def update_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    return await user_service.update_user(
        db,
        user_id=current_user.id,
        email=user_in.email,
        password=user_in.password,
    )
