from datetime import date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId
from database.database import get_database
from models.models import UserResponse, GoalResponse, PatientListItem, PatientStatusResponse
from dependencies import get_current_provider

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
async def get_my_patients(current_user: dict = Depends(get_current_provider)):
    db = get_database()
    patient_providers_collection = db["patient_providers"]
    users_collection = db["users"]
    goals_collection = db["goals"]

    provider_id = str(current_user["_id"])

    assignments = await patient_providers_collection.find(
        {"provider_id": provider_id}
    ).to_list(length=None)

    patients_list = []
    today = date.today()

    for assignment in assignments:
        patient_id = assignment["patient_id"]

        try:
            try:
                patient = await users_collection.find_one({"_id": ObjectId(patient_id)})
            except InvalidId:
                patient = None

            if not patient or patient.get("role") != "patient":
                continue

            today_goal = await goals_collection.find_one({
                "patient_id": str(patient["_id"]),
                "date": today
            })

            patient_item = PatientListItem(
                id=str(patient["_id"]),
                name=patient["name"],
                email=patient["email"],
                today_goal=format_goal(today_goal) if today_goal else None
            )
            patients_list.append(patient_item)
        except Exception:
            continue

    return patients_list


@router.get("/patient/{patient_id}/goals", response_model=List[GoalResponse])
async def get_patient_goals(
    patient_id: str,
    current_user: dict = Depends(get_current_provider)
):
    db = get_database()
    patient_providers_collection = db["patient_providers"]
    users_collection = db["users"]
    goals_collection = db["goals"]

    provider_id = str(current_user["_id"])

    assignment = await patient_providers_collection.find_one({
        "provider_id": provider_id,
        "patient_id": patient_id
    })

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found or not assigned to you"
        )

    try:
        patient = await users_collection.find_one({"_id": ObjectId(patient_id)})
        if not patient or patient.get("role") != "patient":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid patient ID"
        )

    week_ago = date.today() - timedelta(days=7)
    cursor = goals_collection.find({
        "patient_id": patient_id,
        "date": {"$gte": week_ago}
    }).sort("date", -1)

    goals = await cursor.to_list(length=None)
    return [format_goal(goal) for goal in goals]


@router.get("/patient/{patient_id}/status", response_model=PatientStatusResponse)
async def get_patient_status(
    patient_id: str,
    current_user: dict = Depends(get_current_provider)
):
    db = get_database()
    patient_providers_collection = db["patient_providers"]
    users_collection = db["users"]
    goals_collection = db["goals"]

    provider_id = str(current_user["_id"])

    assignment = await patient_providers_collection.find_one({
        "provider_id": provider_id,
        "patient_id": patient_id
    })

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found or not assigned to you"
        )

    try:
        patient = await users_collection.find_one({"_id": ObjectId(patient_id)})
        if not patient or patient.get("role") != "patient":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid patient ID"
        )

    today = date.today()
    today_goal = await goals_collection.find_one({
        "patient_id": patient_id,
        "date": today
    })

    week_ago = date.today() - timedelta(days=7)
    cursor = goals_collection.find({
        "patient_id": patient_id,
        "date": {"$gte": week_ago}
    })

    all_goals = await cursor.to_list(length=None)
    total_steps = sum(goal.get("steps", 0) for goal in all_goals)
    total_sleep = sum(goal.get("sleep_time", 0) for goal in all_goals)
    total_water = sum(goal.get("water_glasses", 0) for goal in all_goals)
    avg_sleep = total_sleep / len(all_goals) if all_goals else 0.0

    return PatientStatusResponse(
        patient=UserResponse(
            id=str(patient["_id"]),
            name=patient["name"],
            email=patient["email"],
            role=patient["role"]
        ),
        today_goal=format_goal(today_goal) if today_goal else None,
        total_steps=total_steps,
        avg_sleep_time=round(avg_sleep, 2),
        total_water_glasses=total_water
    )
