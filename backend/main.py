from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Backend Todo Application API", version="1.0.0")

# Configure CORS for localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers for authentication
    expose_headers=["Access-Control-Allow-Origin"]
)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    from db import create_db_and_tables
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Backend API"}

# Include routes
from routes import tasks
from routes import auth
from src.api.chat_router import router as chat_router
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(chat_router)