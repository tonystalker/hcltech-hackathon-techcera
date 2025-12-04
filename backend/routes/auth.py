from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from database.database import get_database
from models.models import UserCreate, UserResponse, TokenResponse
from dependencies import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_HOURS, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["authentication"])


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + \
            timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    db = get_database()
    users_collection = db["users"]

    normalized_email = user_data.email.lower().strip()
    existing_user = await users_collection.find_one({"email": normalized_email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(user_data.password)
    user_dict = {
        "name": user_data.name,
        "email": normalized_email,
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


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_database()
    users_collection = db["users"]
    tokens_collection = db["tokens"]

    email = form_data.username.lower().strip()
    user = await users_collection.find_one({"email": email})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = str(user["_id"])
    expires_delta = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user_id, "email": user["email"], "role": user["role"]},
        expires_delta=expires_delta
    )

    await tokens_collection.insert_one({
        "user_id": user_id,
        "token": access_token,
        "created_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc) + expires_delta
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }
