
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
)
from app.services import user_service
from app.core.database import get_db
from app.models.user import User

from app.core.auth import get_current_user
from app.core.jwt import create_access_token
from app.core.logging_utils import get_logger
from app.core.exceptions import NotFoundError, ValidationError

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.core.auth import get_current_user
# from app.models.user import User
# from app.db.session import get_db

# router = APIRouter()


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

logger = get_logger(__name__)

@router.get("/me")
def read_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    # Check for existing user (HTTP concern)
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    if result.scalar_one_or_none():
        # raise HTTPException(
        #     status_code=400,
        #     detail="Email already registered",
        # )
        raise ValidationError("Email already registered")

    await user_service.register_user(
        db,
        email=payload.email,
        password=payload.password,
    )
    
    return {"message": "User created"}


@router.post(
    "/login",
)
async def login(
    payload: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    logger.info("authenticating user", extra={"user_email": payload.email,})
    user = await user_service.authenticate_user(
        db,
        email=payload.email,
        password=payload.password,
    )

    token = create_access_token(user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
    }
