from fastapi import APIRouter, Depends, status
from database.database import get_database
from dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(current_user: dict = Depends(get_current_user)):
    db = get_database()
    users_collection = db["users"]
    tokens_collection = db["tokens"]

    user_id = str(current_user["_id"])

    await users_collection.delete_one({"_id": current_user["_id"]})
    await tokens_collection.delete_many({"user_id": user_id})

    return None
