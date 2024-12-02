from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from app.routes import router
from app.database import connect_to_mongo, close_mongo_connection
import os
from app.database import get_database
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Student Management System",
    description="Backend API for managing student records.",
    version="1.0.0",
)

# Redirect root URL to Swagger UI
@app.get("/")
def root():
    return RedirectResponse(url="/docs")

# Include your routes
app.include_router(router)

# Startup event to connect to MongoDB
@app.on_event("startup")
async def startup_db_client():
    mongo_url = os.getenv("MONGO_URL")
    db_name = os.getenv("DB_NAME")
    print(mongo_url, " ", db_name)
    if not mongo_url or not db_name:
        raise ValueError("Environment variables MONGO_URL or DB_NAME are not set.")
    await connect_to_mongo(mongo_url, db_name)

# Shutdown event to disconnect MongoDB
@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

def get_database():
    global db
    if db is None:
        raise ValueError("Database is not initialized. Did you call `connect_to_mongo()`?")
    return db

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
