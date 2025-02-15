from pathlib import Path
import logging
import os
from ultralytics import YOLO
import numpy as np

logger = logging.getLogger(__name__)

class FoodDetector:
    def __init__(self):
        """Initialize the YOLOv8n model for food detection"""
        try:
            # Initialize YOLOv8n model
            self.model = YOLO('yolov8n.pt')
            
            # Cache the class names for food items only
            self.food_classes = {
                idx: name for idx, name in enumerate(self.model.names.values())
                if name in self._get_food_classes()
            }
            
            # Confidence threshold
            self.conf_threshold = float(os.getenv('DETECTION_CONFIDENCE', 0.3))
            
            logger.info("Food detection system initialized with YOLOv8n model")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize food detection system: {str(e)}")

    def _get_food_classes(self):
        """Return a set of COCO food-related class names"""
        return {
            'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
            'donut', 'cake', 'bowl', 'dining table', 'food', 'fruit', 'vegetable'
        }

    def detect(self, image_path: str) -> list:
        """
        Detect food items in an image using YOLOv8n
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            list: List of detected food items with confidence scores
        """
        try:
            if not Path(image_path).exists():
                raise FileNotFoundError(f"Image not found: {image_path}")

            # Run inference
            results = self.model(image_path, conf=self.conf_threshold)[0]
            
            # Filter and format detections
            detections = []
            for box in results.boxes:
                class_id = int(box.cls[0])
                if class_id in self.food_classes:
                    conf = float(box.conf[0])
                    class_name = self.food_classes[class_id]
                    detections.append(f"{class_name} ({conf:.2f})")
            
            return detections if detections else ["No food items detected"]
            
        except Exception as e:
            raise RuntimeError(f"Error processing image: {str(e)}")
