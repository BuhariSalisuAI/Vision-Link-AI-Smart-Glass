# test_object_detection.py
# Vision-Link AI Smart Glass - Test Object Detection Module

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
from app.core.object_detection import detect_objects, ObjectDetector

def test_with_camera():
    """
    Test object detection with live camera
    """
    print("=== Testing Object Detection with Camera ===")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return
    
    print("Camera opened. Press 'q' to quit.")
    
    detector = ObjectDetector()
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Cannot read frame")
            break
        
        # Detect objects
        results = detector.detect(frame)
        
        # Draw results on frame
        for obj in results:
            x, y, w, h = obj['bbox']
            label = f"{obj['class']} ({obj['confidence']:.2f})"
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Display
        cv2.imshow('Object Detection Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Camera test completed.")

def test_with_image(image_path):
    """
    Test object detection with a single image
    """
    print(f"=== Testing with Image: {image_path} ===")
    
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Cannot load image {image_path}")
        return
    
    detector = ObjectDetector()
    results = detector.detect(image)
    
    print(f"Detected {len(results)} objects:")
    for obj in results:
        print(f"  - {obj['class']}: {obj['confidence']:.2f}")
    
    # Draw and save result
    for obj in results:
        x, y, w, h = obj['bbox']
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        label = f"{obj['class']} ({obj['confidence']:.2f})"
        cv2.putText(image, label, (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    output_path = "test_detection_result.jpg"
    cv2.imwrite(output_path, image)
    print(f"Result saved to {output_path}")

def test_performance():
    """
    Test detection speed/performance
    """
    print("\n=== Testing Performance ===")
    
    import time
    import numpy as np
    
    detector = ObjectDetector()
    
    # Create dummy image
    dummy_image = np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8)
    
    # Warm up
    detector.detect(dummy_image)
    
    # Time multiple runs
    times = []
    for _ in range(10):
        start = time.time()
        detector.detect(dummy_image)
        times.append(time.time() - start)
    
    avg_time = sum(times) / len(times)
    print(f"Average detection time: {avg_time:.3f} seconds")
    print(f"FPS: {1/avg_time:.1f}")

if __name__ == "__main__":
    print("Vision-Link AI - Object Detection Tests")
    print("=" * 40)
    
    # Choose test
    print("1. Test with camera")
    print("2. Test with image file")
    print("3. Test performance")
    
    choice = input("Enter choice (1-3): ")
    
    if choice == '1':
        test_with_camera()
    elif choice == '2':
        path = input("Enter image path: ")
        test_with_image(path)
    elif choice == '3':
        test_performance()
    else:
        print("Invalid choice")
