from fastapi import APIRouter, HTTPException, status
from database.database import get_database
from models.models import UserCreate, UserResponse
from dependencies import hash_password

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    db = get_database()
    
    normalized_email = user_data.email.lower().strip()
    if await db["users"].find_one({"email": normalized_email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_dict = {
        "name": user_data.name,
        "email": normalized_email,
        "role": user_data.role,
        "password": hash_password(user_data.password)
    }

    result = await db["users"].insert_one(user_dict)
    return UserResponse(id=str(result.inserted_id), name=user_dict["name"], email=user_dict["email"], role=user_dict["role"])
