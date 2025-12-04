from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.database import connect_to_mongo, close_mongo_connection
from routes.auth import router as auth_router
from routes.user import router as user_router
from routes.goals import router as goals_router
from routes.credentials import router as credentials_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
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

@app.get("/")
async def root():
    return {"message": "Healthcare Wellness & Preventive Care Portal API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
