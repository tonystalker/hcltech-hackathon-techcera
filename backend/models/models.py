from datetime import date
from typing import Optional
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


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class GoalCreate(BaseModel):
    steps: int = Field(..., ge=0, description="Number of steps walked")
    sleep_time: float = Field(..., ge=0, le=24, description="Hours of sleep")
    water_glasses: int = Field(..., ge=0,
                               description="Number of glasses of water consumed")


class GoalResponse(BaseModel):
    id: str
    patient_id: str
    date: date
    steps: int
    sleep_time: float
    water_glasses: int

    class Config:
        allow_population_by_field_name = True


class PatientStatusResponse(BaseModel):
    patient: UserResponse
    today_goal: Optional[GoalResponse] = None
    total_steps: int = 0
    avg_sleep_time: float = 0.0
    total_water_glasses: int = 0


class PatientListItem(BaseModel):
    id: str
    name: str
    email: str
    today_goal: Optional[GoalResponse] = None
