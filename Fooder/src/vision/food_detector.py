import torch
import cv2
import numpy as np
from pathlib import Path

class FoodDetector:
    def __init__(self):
        """Initialize the YOLOv5 model for food detection"""
        # Load YOLOv5 model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        
        # Define food-related classes from COCO dataset
        self.food_classes = [
            'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 
            'pizza', 'donut', 'cake'
        ]
        
        # Set model parameters
        self.model.conf = 0.3  # Confidence threshold
        self.model.classes = [self.model.names.index(c) for c in self.food_classes if c in self.model.names]

    def detect(self, image_path: str) -> list:
        """
        Detect food items in an image
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            list: List of detected food items
        """
        # Ensure the image file exists
        img_path = Path(image_path)
        if not img_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Read and process the image
        img = cv2.imread(str(img_path))
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")

        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Perform detection
        results = self.model(img)

        # Extract detected food items
        detected_items = []
        for pred in results.pred[0]:
            class_id = int(pred[5])
            class_name = self.model.names[class_id]
            if class_name in self.food_classes:
                confidence = float(pred[4])
                if class_name not in detected_items:  # Avoid duplicates
                    detected_items.append(class_name)

        return detected_items

    def _preprocess_image(self, img):
        """
        Preprocess image for model input
        
        Args:
            img (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Preprocessed image
        """
        # Resize if needed
        return cv2.resize(img, (640, 640))
