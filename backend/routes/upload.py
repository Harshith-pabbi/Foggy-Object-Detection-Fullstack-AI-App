from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
import uuid
import os
import shutil

from backend.database import get_db
from backend import models
from backend import schemas
from backend.ai.pipeline import process_video

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/", response_model=schemas.JobResponse)
def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only video files are supported.")

    job_id = str(uuid.uuid4())
    input_path = os.path.join("uploads", f"{job_id}_{file.filename}")
    
    # Save the file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create job in database
    db_job = models.Job(
        job_id=job_id,
        status="pending",
        input_file_path=input_path
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # Trigger background processing
    background_tasks.add_task(process_video, job_id, input_path)

    return {"job_id": job_id, "status": "pending", "message": "Video uploaded successfully. Processing started."}
