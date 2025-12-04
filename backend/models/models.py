from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = Field(..., pattern="^(patient|provider)$")

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str

    class Config:
        allow_population_by_field_name = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

