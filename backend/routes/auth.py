import os
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, status
from jose import jwt
import bcrypt
from database.database import get_database
from models.models import UserCreate, UserResponse, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["authentication"])

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    db = get_database()
    users_collection = db["users"]
    
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(user_data.password)
    user_dict = {
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role,
        "password": hashed_password
    }
    
    result = await users_collection.insert_one(user_dict)
    user_dict["_id"] = result.inserted_id
    
    return UserResponse(
        id=str(user_dict["_id"]),
        name=user_dict["name"],
        email=user_dict["email"],
        role=user_dict["role"]
    )

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    db = get_database()
    users_collection = db["users"]
    tokens_collection = db["tokens"]
    
    user = await users_collection.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    user_id = str(user["_id"])
    expires_delta = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user_id, "email": user["email"], "role": user["role"]},
        expires_delta=expires_delta
    )
    
    expires_at = datetime.now(timezone.utc) + expires_delta
    token_doc = {
        "user_id": user_id,
        "token": access_token,
        "created_at": datetime.now(timezone.utc),
        "expires_at": expires_at
    }
    
    await tokens_collection.insert_one(token_doc)
    
    user_response = UserResponse(
        id=user_id,
        name=user["name"],
        email=user["email"],
        role=user["role"]
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

