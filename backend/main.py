from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.database import connect_to_mongo, close_mongo_connection, check_mongo_connection
from routes.auth import router as auth_router
from routes.user import router as user_router
from routes.goals import router as goals_router
from routes.credentials import router as credentials_router
from routes.provider import router as provider_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_to_mongo()
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        print("Server starting without database connection")
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Healthcare Wellness & Preventive Care Portal",
    description="API for tracking patient wellness goals and provider monitoring",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(goals_router)
app.include_router(credentials_router)
app.include_router(provider_router)


@app.get("/")
async def root():
    return {"message": "Healthcare Wellness & Preventive Care Portal API"}


@app.get("/health")
async def health_check():
    db_status = await check_mongo_connection()
    if not db_status["connected"]:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {db_status.get('error', 'Unknown')}")
    return {"status": "healthy", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
