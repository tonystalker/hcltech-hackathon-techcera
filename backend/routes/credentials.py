from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from database.database import get_database
from dependencies import get_current_user, hash_password
from models.models import UserUpdate, UserResponse

router = APIRouter(prefix="/credentials", tags=["credentials"])

@router.put("/modify", response_model=UserResponse)
async def modify_credentials(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    users_collection = db["users"]

    update_data = {}

    if user_update.name is not None:
        update_data["name"] = user_update.name

    if user_update.email is not None:
        existing_user = await users_collection.find_one({"email": user_update.email.lower().strip()})
        if existing_user and str(existing_user["_id"]) != str(current_user["_id"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        update_data["email"] = user_update.email.lower().strip()

    if user_update.password is not None:
        update_data["password"] = hash_password(user_update.password)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    update_data["updated_at"] = datetime.now(timezone.utc)

    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$set": update_data}
    )

    updated_user = await users_collection.find_one({"_id": current_user["_id"]})

    return UserResponse(
        id=str(updated_user["_id"]),
        name=updated_user["name"],
        email=updated_user["email"],
        role=updated_user["role"]
    )

