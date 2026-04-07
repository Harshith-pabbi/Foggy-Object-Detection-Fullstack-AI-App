from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str

class DetectionResult(BaseModel):
    job_id: str
    status: str
    input_url: Optional[str] = None
    output_url: Optional[str] = None
    detections: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True
