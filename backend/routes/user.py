from typing import List
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId
from database.database import get_database
from models.models import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserResponse])
async def list_users():
    db = get_database()
    users = await db["users"].find({}, {"password": 0}).to_list(length=None)
    return [UserResponse(id=str(u["_id"]), name=u["name"], email=u["email"], role=u["role"]) for u in users]


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    db = get_database()
    try:
        result = await db["users"].delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await db["tokens"].delete_many({"user_id": user_id})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user ID")
