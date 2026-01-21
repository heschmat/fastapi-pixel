from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.users import UserOut
from app.schemas.auth import UserRegister, TokenRefresh
from app.models.user import User
from app.services import auth_service
from app.core.auth import get_current_user_from_token


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

# logger = get_logger(__name__)

@router.get("/me")
def read_me(
    current_user: User = Depends(get_current_user_from_token),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }


# @router.post(
#     "/register",
#     response_model=UserOut,
#     status_code=status.HTTP_201_CREATED,
# )
# async def register(
#     payload: RegisterRequest,
#     request: Request,
#     db: AsyncSession = Depends(get_db),
# ):
    
#     created = await user_service.register_user(
#         db,
#         email=payload.email,
#         password=payload.password,
#     )
    
#     return {"message": "User created"}


# @router.post(
#     "/login",
# )
# async def login(
#     payload: LoginRequest,
#     request: Request,
#     db: AsyncSession = Depends(get_db),
# ):
#     logger.info("authenticating user", extra={"user_email": payload.email,})
#     user = await user_service.authenticate_user(
#         db,
#         email=payload.email,
#         password=payload.password,
#     )

#     token = create_access_token(user.id)
#     return {
#         "access_token": token,
#         "token_type": "bearer",
#     }


# @router.post("/login")
# async def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: AsyncSession = Depends(get_db),
# ):
#     access_token = await auth_service.login(
#         db,
#         email=form_data.username,
#         password=form_data.password,
#     )

#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#     }


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_in: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    return await auth_service.register_user(
        db,
        email=user_in.email,
        password=user_in.password,
    )


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    access, refresh = await auth_service.authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password,
    )

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
    }


# @router.post("/refresh")
# async def refresh(
#     user_id: int,
#     refresh_token: str,
#     db: AsyncSession = Depends(get_db),
# ):
#     access, refresh = await auth_service.refresh_tokens(
#         db,
#         user_id=user_id,
#         refresh_token=refresh_token,
#     )

#     return {
#         "access_token": access,
#         "refresh_token": refresh,
#     }

@router.post("/refresh")
async def refresh(
    token_in: TokenRefresh,
    db: AsyncSession = Depends(get_db),
):
    access, refresh = await auth_service.rotate_refresh_token(
        db,
        user_id=token_in.user_id,
        refresh_token=token_in.refresh_token,
    )

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
    }
