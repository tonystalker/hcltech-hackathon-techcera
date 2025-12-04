from typing import List
from fastapi import APIRouter, Depends, status
from database.database import get_database
from models.models import UserResponse
from dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserResponse])
async def list_users():
    db = get_database()
    users = await db["users"].find({}, {"password": 0}).to_list(length=None)
    return [UserResponse(id=str(u["_id"]), name=u["name"], email=u["email"], role=u["role"]) for u in users]

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(current_user: dict = Depends(get_current_user)):
    db = get_database()
    users_collection = db["users"]
    tokens_collection = db["tokens"]

    user_id = str(current_user["_id"])

    await users_collection.delete_one({"_id": current_user["_id"]})
    await tokens_collection.delete_many({"user_id": user_id})

    return None
