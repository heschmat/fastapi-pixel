class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
