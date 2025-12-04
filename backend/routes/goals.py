from datetime import date, datetime, timedelta, timezone
from typing import List, Optional
from fastapi import APIRouter, status
from database.database import get_database
from models.models import GoalCreate, GoalResponse

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


@router.post("/{patient_id}", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def add_goal(patient_id: str, goal_data: GoalCreate):
    db = get_database()
    goals_collection = db["goals"]
    today = date.today()

    existing_goal = await goals_collection.find_one({"patient_id": patient_id, "date": today})

    goal_dict = {
        "patient_id": patient_id,
        "date": today,
        "steps": goal_data.steps,
        "sleep_time": goal_data.sleep_time,
        "water_glasses": goal_data.water_glasses,
        "created_at": datetime.now(timezone.utc)
    }

    if existing_goal:
        await goals_collection.update_one(
            {"_id": existing_goal["_id"]},
            {"$set": {"steps": goal_data.steps, "sleep_time": goal_data.sleep_time, "water_glasses": goal_data.water_glasses, "updated_at": datetime.now(timezone.utc)}}
        )
        goal_dict["_id"] = existing_goal["_id"]
    else:
        result = await goals_collection.insert_one(goal_dict)
        goal_dict["_id"] = result.inserted_id

    return format_goal(goal_dict)


@router.get("/{patient_id}/today", response_model=Optional[GoalResponse])
async def get_today_goal(patient_id: str):
    db = get_database()
    goal = await db["goals"].find_one({"patient_id": patient_id, "date": date.today()})
    return format_goal(goal) if goal else None


@router.get("/{patient_id}/history", response_model=List[GoalResponse])
async def get_goal_history(patient_id: str):
    db = get_database()
    week_ago = date.today() - timedelta(days=7)
    cursor = db["goals"].find({"patient_id": patient_id, "date": {"$gte": week_ago}}).sort("date", -1)
    goals = await cursor.to_list(length=None)
    return [format_goal(goal) for goal in goals]
