from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class TokenRefresh(BaseModel):
    user_id: int = Field(gt=0)
    refresh_token: str = Field(min_length=1)
