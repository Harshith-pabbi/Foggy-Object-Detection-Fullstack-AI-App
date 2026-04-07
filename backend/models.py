from sqlalchemy import Column, Integer, String, Float, JSON
from backend.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    input_file_path = Column(String)
    output_file_path = Column(String, nullable=True)
    detections = Column(JSON, nullable=True)  # Store detection summaries
