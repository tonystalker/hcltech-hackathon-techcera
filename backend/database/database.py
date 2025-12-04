import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None

db = MongoDB()


async def connect_to_mongo():
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb+srv://abhinavpandey1230:b1o5@cluster0.p5tcj7g.mongodb.net/")
    db.client = AsyncIOMotorClient(mongodb_uri)
    database_name = os.getenv("DATABASE_NAME", "healthcare_portal")
    await db.client.admin.command('ping')
    print(f"Connected to MongoDB: {database_name}")
    return db.client[database_name]


async def close_mongo_connection():
    if db.client:
        db.client.close()


def get_database():
    database_name = os.getenv("DATABASE_NAME", "healthcare_portal")
    if db.client is None:
        raise RuntimeError("Database not connected")
    return db.client[database_name]


async def check_mongo_connection() -> dict:
    try:
        if db.client is None:
            return {"connected": False, "error": "Client not initialized"}
        await db.client.admin.command('ping')
        return {"connected": True}
    except Exception as e:
        return {"connected": False, "error": str(e)}
