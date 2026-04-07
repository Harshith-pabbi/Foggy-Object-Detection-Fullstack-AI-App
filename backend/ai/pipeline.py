import os
import cv2
from sqlalchemy.orm import Session
from backend.models import Job
from backend.database import SessionLocal
from .dehaze_aodnet import dehaze_video_frame
from .detect_yolo import detect_objects

def process_video(job_id: str, input_path: str):
    db = SessionLocal()
    try:
        # Update status
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if job:
            job.status = "processing"
            db.commit()

        # Define outputs
        output_filename = f"dehazed_{job_id}.mp4"
        output_path = os.path.join("outputs", output_filename)
        
        cap = cv2.VideoCapture(input_path)
        
        if not cap.isOpened():
            raise Exception("Cannot open video stream or file")
            
        # Extract video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        
        # Use mp4v which natively encodes into mp4 wrapper compatible format
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        all_detections = []
        
        # Hard stop limit for web testing (protects CPU)
        max_test_frames = 600 # Approx 20s of 30fps
        frame_counter = 0

        while True:
            ret, frame = cap.read()
            if not ret or frame_counter >= max_test_frames:
                break
                
            frame_counter += 1
            
            # Step 1: Dehaze the raw frame
            dehazed = dehaze_video_frame(frame)
            
            # Step 2: Detect objects in the dehazed frame
            annotated_frame, frame_detections = detect_objects(dehazed)
            
            # Aggregate detections
            all_detections.extend(frame_detections)
            
            # Step 3: Write out to disk
            out.write(annotated_frame)

        cap.release()
        out.release()
        
        # Calculate most significant unique detections (max 10 rows for UI presentation)
        # Use dictionary to capture highest confidence per class
        best_classes = {}
        for d in all_detections:
            c = d["class"]
            if c not in best_classes or d["confidence"] > best_classes[c]["confidence"]:
                best_classes[c] = d
        
        summary = sorted(list(best_classes.values()), key=lambda x: x["confidence"], reverse=True)[:10]

        # Final DB completion write-back
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if job:
            job.status = "completed"
            job.output_file_path = output_path
            job.detections = summary
            db.commit()

    except Exception as e:
        print(f"Error in processing video: {str(e)}")
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if job:
            job.status = "failed"
            db.commit()
    finally:
        db.close()
