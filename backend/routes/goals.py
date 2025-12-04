from datetime import date, datetime, timedelta, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from database.database import get_database
from models.models import GoalCreate, GoalResponse
from dependencies import get_current_patient

router = APIRouter(prefix="/goals", tags=["goals"])


def format_goal(goal_dict: dict) -> GoalResponse:
    return GoalResponse(
        id=str(goal_dict["_id"]),
        patient_id=goal_dict["patient_id"],
        date=goal_dict["date"],
        steps=goal_dict["steps"],
        sleep_time=goal_dict["sleep_time"],
        water_glasses=goal_dict.get("water_glasses", 0)
    )


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def add_goal(goal_data: GoalCreate, current_user: dict = Depends(get_current_patient)):
    db = get_database()
    goals_collection = db["goals"]

    user_id = str(current_user["_id"])
    today = date.today()

    existing_goal = await goals_collection.find_one({
        "patient_id": user_id,
        "date": today
    })

    goal_dict = {
        "patient_id": user_id,
        "date": today,
        "steps": goal_data.steps,
        "sleep_time": goal_data.sleep_time,
        "water_glasses": goal_data.water_glasses,
        "created_at": datetime.now(timezone.utc)
    }

    if existing_goal:
        await goals_collection.update_one(
            {"_id": existing_goal["_id"]},
            {"$set": {
                "steps": goal_data.steps,
                "sleep_time": goal_data.sleep_time,
                "water_glasses": goal_data.water_glasses,
                "updated_at": datetime.now(timezone.utc)
            }}
        )
        goal_dict["_id"] = existing_goal["_id"]
    else:
        result = await goals_collection.insert_one(goal_dict)
        goal_dict["_id"] = result.inserted_id

    return format_goal(goal_dict)


@router.get("/today", response_model=Optional[GoalResponse])
async def get_today_goal(current_user: dict = Depends(get_current_patient)):
    db = get_database()
    goals_collection = db["goals"]

    user_id = str(current_user["_id"])
    today = date.today()

    goal = await goals_collection.find_one({
        "patient_id": user_id,
        "date": today
    })

    if not goal:
        return None

    return format_goal(goal)


@router.get("/history", response_model=List[GoalResponse])
async def get_goal_history(current_user: dict = Depends(get_current_patient)):
    db = get_database()
    goals_collection = db["goals"]

    user_id = str(current_user["_id"])
    week_ago = date.today() - timedelta(days=7)

    cursor = goals_collection.find({
        "patient_id": user_id,
        "date": {"$gte": week_ago}
    }).sort("date", -1)

    goals = await cursor.to_list(length=None)
    return [format_goal(goal) for goal in goals]
