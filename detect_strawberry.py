#!/usr/bin/env python3
"""
Simple Strawberry Disease Detection Script
No web server required - just run and provide image path
"""

import sys
from pathlib import Path
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np

def load_model():
    """Load the trained model"""
    root = Path(__file__).resolve().parent
    weights_path = root / "runs" / "yolov8n-strawberry" / "weights" / "best.pt"
    
    if not weights_path.exists():
        print(f"❌ Model weights not found at: {weights_path}")
        print("Please train the model first using: python train_yolov8.py")
        return None
    
    print(f"✅ Loading model from: {weights_path}")
    return YOLO(str(weights_path))

def detect_diseases(model, image_path):
    """Detect diseases in strawberry image"""
    try:
        # Load and process image
        image = cv2.imread(str(image_path))
        if image is None:
            print(f"❌ Could not load image: {image_path}")
            return None
        
        # Run detection
        results = model(image)
        
        # Process results
        detections = []
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    # Get class name and confidence
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    class_name = model.names[class_id]
                    
                    detections.append({
                        'class': class_name,
                        'confidence': confidence,
                        'bbox': box.xyxy[0].tolist()
                    })
        
        return detections, image
        
    except Exception as e:
        print(f"❌ Error during detection: {e}")
        return None, None

def main():
    print("🍓 Strawberry Disease Detection")
    print("=" * 40)
    
    # Load model
    model = load_model()
    if model is None:
        return
    
    # Get image path from command line or prompt
    if len(sys.argv) > 1:
        image_path = Path(sys.argv[1])
    else:
        image_path_str = input("Enter path to strawberry image: ").strip()
        image_path = Path(image_path_str)
    
    if not image_path.exists():
        print(f"❌ Image not found: {image_path}")
        return
    
    print(f"🔍 Analyzing: {image_path.name}")
    
    # Run detection
    result = detect_diseases(model, image_path)
    if result is None:
        return
    
    detections, image = result
    
    # Display results
    print("\n📊 Detection Results:")
    print("-" * 30)
    
    if not detections:
        print("✅ HEALTHY - No diseases detected!")
    else:
        print("❌ NOT HEALTHY - Diseases detected:")
        for det in detections:
            print(f"  • {det['class']} (confidence: {det['confidence']:.2f})")
    
    # Save result image with annotations
    if detections and image is not None:
        # Draw bounding boxes
        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            label = f"{det['class']}: {det['confidence']:.2f}"
            cv2.putText(image, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Save annotated image
        output_path = image_path.parent / f"{image_path.stem}_detected{image_path.suffix}"
        cv2.imwrite(str(output_path), image)
        print(f"\n💾 Annotated image saved: {output_path}")

if __name__ == "__main__":
    main()
