from ultralytics import YOLO
import numpy as np
from PIL import Image
import cv2

# Load YOLO model
model = YOLO("models/yolov8n.pt")

def detect_objects(image):
    """
    Detect objects in an image using the YOLOv8 model.
    :param image: Input image (NumPy array).
    :return: List of detections and image with bounding boxes.
    """
    np_image = np.array(image)
    results = model.predict(np_image, conf=0.5)
    
    detections = [
        {
            "coords": [int(x) for x in box.xyxy[0].tolist()],
            "class": int(box.cls),
            "confidence": float(box.conf)
        }
        for result in results
        for box in result.boxes
    ]
    return detections

def remove_detected_objects(image: Image.Image, detections: list) -> Image.Image:
    """
    Remove detected objects from the background by masking and inpainting.
    :param image: Input image (PIL Image).
    :param detections: List of detections containing bounding box coordinates of objects.
    :return: Image with the objects removed.
    """
    np_image = np.array(image)
    mask = np.zeros(np_image.shape[:2], dtype=np.uint8)

    for detection in detections:
        x1, y1, x2, y2 = detection["coords"]
        mask[y1:y2, x1:x2] = 255

    inpainted_image = cv2.inpaint(np_image, mask, 3, cv2.INPAINT_TELEA)
    return Image.fromarray(inpainted_image)
