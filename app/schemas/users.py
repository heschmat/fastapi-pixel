from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


# from pydantic import BaseModel, EmailStr, Field

# class RegisterRequest(BaseModel):
#     email: EmailStr
#     password: str = Field(min_length=8)

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str
