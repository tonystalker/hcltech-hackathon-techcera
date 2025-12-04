from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId
from database.database import get_database
from models.models import UserResponse, GoalResponse, PatientListItem, PatientStatusResponse

router = APIRouter(prefix="/provider", tags=["provider"])


def format_goal(goal_dict: dict) -> GoalResponse:
    return GoalResponse(
        id=str(goal_dict["_id"]),
        patient_id=goal_dict["patient_id"],
        date=goal_dict["date"],
        steps=goal_dict["steps"],
        sleep_time=goal_dict["sleep_time"],
        water_glasses=goal_dict.get("water_glasses", 0)
    )


@router.get("/patients", response_model=List[PatientListItem])
async def get_all_patients():
    db = get_database()
    patients = await db["users"].find({"role": "patient"}).to_list(length=None)
    today = date.today()
    
    result = []
    for p in patients:
        today_goal = await db["goals"].find_one({"patient_id": str(p["_id"]), "date": today})
        result.append(PatientListItem(
            id=str(p["_id"]),
            name=p["name"],
            email=p["email"],
            today_goal=format_goal(today_goal) if today_goal else None
        ))
    return result


@router.get("/patient/{patient_id}/goals", response_model=List[GoalResponse])
async def get_patient_goals(patient_id: str):
    db = get_database()
    
    try:
        patient = await db["users"].find_one({"_id": ObjectId(patient_id)})
        if not patient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid patient ID")

    week_ago = date.today() - timedelta(days=7)
    goals = await db["goals"].find({"patient_id": patient_id, "date": {"$gte": week_ago}}).sort("date", -1).to_list(length=None)
    return [format_goal(g) for g in goals]


@router.get("/patient/{patient_id}/status", response_model=PatientStatusResponse)
async def get_patient_status(patient_id: str):
    db = get_database()
    
    try:
        patient = await db["users"].find_one({"_id": ObjectId(patient_id)})
        if not patient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid patient ID")

    today = date.today()
    today_goal = await db["goals"].find_one({"patient_id": patient_id, "date": today})

    week_ago = today - timedelta(days=7)
    all_goals = await db["goals"].find({"patient_id": patient_id, "date": {"$gte": week_ago}}).to_list(length=None)
    
    total_steps = sum(g.get("steps", 0) for g in all_goals)
    total_sleep = sum(g.get("sleep_time", 0) for g in all_goals)
    total_water = sum(g.get("water_glasses", 0) for g in all_goals)
    avg_sleep = total_sleep / len(all_goals) if all_goals else 0.0

    return PatientStatusResponse(
        patient=UserResponse(id=str(patient["_id"]), name=patient["name"], email=patient["email"], role=patient["role"]),
        today_goal=format_goal(today_goal) if today_goal else None,
        total_steps=total_steps,
        avg_sleep_time=round(avg_sleep, 2),
        total_water_glasses=total_water
    )
