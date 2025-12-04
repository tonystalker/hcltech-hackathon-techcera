from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = Field(..., pattern="^(patient|provider)$")

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserResponse(UserBase):
    id: str

    class Config:
        allow_population_by_field_name = True

class GoalBase(BaseModel):
    patient_id: str
    date: date
    steps: int = Field(..., ge=0)
    water_glasses: int = Field(..., ge=0)

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class GoalResponse(GoalBase):
    id: str

    class Config:
        allow_population_by_field_name = True

class PatientProviderBase(BaseModel):
    patient_id: str
    provider_id: str

class PatientProvider(PatientProviderBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ReminderBase(BaseModel):
    patient_id: str
    message: str
    due_date: datetime

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ReminderResponse(ReminderBase):
    id: str

    class Config:
        allow_population_by_field_name = True

