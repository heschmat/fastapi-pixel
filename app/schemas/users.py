from pydantic import BaseModel, EmailStr, Field, ConfigDict

# class RegisterRequest(BaseModel):
#     email: EmailStr
#     password: str = Field(min_length=8)

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr



class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8)
