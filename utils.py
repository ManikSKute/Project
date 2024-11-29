import os
import cv2
import numpy as np
from PIL import Image

def save_image(image: np.ndarray, output_path: str):
    """
    Save the image to the specified path.
    :param image: Image to save (NumPy array).
    :param output_path: Path to save the image.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

def draw_bounding_boxes(image: np.ndarray, detections: list):
    """
    Draw bounding boxes on an image.
    :param image: Input image (NumPy array).
    :param detections: List of detections containing bounding box coordinates and labels.
    :return: Image with bounding boxes drawn.
    """
    for detection in detections:
        x1, y1, x2, y2 = detection["coords"]
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"Class {detection['class']} ({detection['confidence']:.2f})"
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image
