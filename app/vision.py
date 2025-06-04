# app/vision.py
import io
import os
from ultralytics import YOLO
import numpy as np
from PIL import Image
import cv2
from fastapi import HTTPException

# Load the pretrained YOLOv5s model once at startup
model = YOLO("yolov5su.pt")  # this will download weights automatically if not present

# Map COCO class IDs to human-friendly names you care about
# YOLOv5s is trained on COCO; classes like "book", "cup", "cell phone" exist.
# You can filter to just desk-related items if you want.
DESK_CLASSES = {
    "book", "cell phone", "cup", "laptop", "keyboard", "mouse", "bottle", "chair", "bowl", "tv"
}

async def detect_clutter(image_bytes: bytes):
    """
    Runs YOLOv5 inference on an image asynchronously
    """
    try:
        # Load image from bytes
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Failed to decode image")

        # Run inference
        results = model(img)

        counts = {}
        annotated_img = img.copy()

        # Loop over detected objects
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                cls_name = model.names[cls_id]
                
                # Only count if confidence > 0.5
                if conf > 0.5 and cls_name in DESK_CLASSES:
                    counts[cls_name] = counts.get(cls_name, 0) + 1
                    
                    # Draw box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Add label with confidence
                    label = f"{cls_name} {conf:.2f}"
                    cv2.putText(
                        annotated_img,
                        label,
                        (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )

        # Encode annotated image
        success, buffer = cv2.imencode('.jpg', annotated_img)
        if not success:
            raise ValueError("Failed to encode annotated image")

        return {
            "counts": counts,
            "annotated_image": buffer.tobytes(),
            "success": True
        }

    except Exception as e:
        print(f"Error in detect_clutter: {str(e)}")
        raise
