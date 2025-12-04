
import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None

db = MongoDB()

async def connect_to_mongo():
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db.client = AsyncIOMotorClient(mongodb_uri)
    database_name = os.getenv("DATABASE_NAME", "healthcare_portal")
    return db.client[database_name]

async def close_mongo_connection():
    if db.client:
        db.client.close()

def get_database():
    database_name = os.getenv("DATABASE_NAME", "healthcare_portal")
    if db.client is None:
        raise RuntimeError("Database not connected. Call connect_to_mongo() first.")
    return db.client[database_name]


