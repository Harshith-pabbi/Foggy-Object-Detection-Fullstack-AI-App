from ultralytics import YOLO
import cv2

# Initialize the model once so it is loaded safely in memory and downloads automatically if needed
model = YOLO("yolov8n.pt")

def detect_objects(frame):
    """
    YOLOv8 Detection integration.
    Analyzes the frame, draws bounding boxes, and returns the annotated frame + raw detection data.
    """
    # The `verbose=False` prevents terminal spam per frame iteration
    results = model(frame, verbose=False)
    detections = []
    
    annotated_frame = frame.copy()
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Get coordinates, confidence, and class
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls_id = int(box.cls[0].item())
            class_name = model.names[cls_id]
            
            # Format boxes for UI and Drawing
            start_point = (int(x1), int(y1))
            end_point = (int(x2), int(y2))
            
            # Draw a beautiful green box with label
            cv2.rectangle(annotated_frame, start_point, end_point, (0, 255, 0), 2)
            
            label = f"{class_name} {conf:.2f}"
            (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(annotated_frame, (int(x1), int(y1) - 20), (int(x1) + text_w, int(y1)), (0, 255, 0), -1)
            cv2.putText(annotated_frame, label, (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            
            detections.append({
                "class": class_name,
                "confidence": round(conf, 2),
                "bbox": [int(x1), int(y1), int(x2), int(y2)]
            })
            
    return annotated_frame, detections
