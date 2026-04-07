from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from backend.database import engine, Base
from backend.routes import upload, results

# Create tables
Base.metadata.create_all(bind=engine)

# Setup directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

app = FastAPI(
    title="Foggy Detection API",
    description="API for processing videos for foggy weather object detection.",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(results.router)

# Mount files for serving the videos
app.mount("/files/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/files/outputs", StaticFiles(directory="outputs"), name="outputs")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Foggy Detection API"}
