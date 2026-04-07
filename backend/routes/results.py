from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models
from backend import schemas
from backend.database import get_db

router = APIRouter(prefix="/results", tags=["Results"])

@router.get("/{job_id}", response_model=schemas.DetectionResult)
def get_results(job_id: str, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.job_id,
        "status": job.status,
        "input_url": f"/files/{job.input_file_path}".replace("\\\\", "/") if job.input_file_path else None,
        "output_url": f"/files/{job.output_file_path}".replace("\\\\", "/") if job.output_file_path else None,
        "detections": job.detections
    }
