from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId
from database.database import get_database
from dependencies import hash_password
from models.models import UserUpdate, UserResponse

router = APIRouter(prefix="/credentials", tags=["credentials"])


@router.put("/{user_id}", response_model=UserResponse)
async def modify_credentials(user_id: str, user_update: UserUpdate):
    db = get_database()
    
    try:
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user ID")

    update_data = {}
    if user_update.name:
        update_data["name"] = user_update.name
    if user_update.email:
        existing = await db["users"].find_one({"email": user_update.email.lower().strip()})
        if existing and str(existing["_id"]) != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        update_data["email"] = user_update.email.lower().strip()
    if user_update.password:
        update_data["password"] = hash_password(user_update.password)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    update_data["updated_at"] = datetime.now(timezone.utc)
    await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    
    updated = await db["users"].find_one({"_id": ObjectId(user_id)})
    return UserResponse(id=str(updated["_id"]), name=updated["name"], email=updated["email"], role=updated["role"])
