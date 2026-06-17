# camera_module.py
# Vision-Link AI Smart Glass - Camera Hardware Module
# Controls Raspberry Pi Camera

import cv2
import config

class CameraModule:
    def __init__(self):
        self.camera = None
        self.resolution = config.CAMERA_SETTINGS['resolution']
        self.fps = config.CAMERA_SETTINGS['fps']
        
    def initialize(self):
        """
        Initialize and open camera
        """
        self.camera = cv2.VideoCapture(0)  # 0 = default camera
        
        if not self.camera.isOpened():
            print("Error: Cannot open camera")
            return False
        
        # Set camera properties
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        self.camera.set(cv2.CAP_PROP_FPS, self.fps)
        
        print("Camera initialized successfully")
        return True
    
    def capture_frame(self):
        """
        Capture a single frame
        Returns: numpy array (image) or None
        """
        if self.camera is None:
            return None
            
        ret, frame = self.camera.read()
        
        if ret:
            return frame
        else:
            print("Error: Failed to capture frame")
            return None
    
    def capture_photo(self, filename=None):
        """
        Capture and save a photo
        """
        frame = self.capture_frame()
        
        if frame is not None and filename:
            cv2.imwrite(filename, frame)
            print(f"Photo saved: {filename}")
            return True
        
        return False
    
    def release(self):
        """
        Release camera resources
        """
        if self.camera:
            self.camera.release()
            self.camera = None
            print("Camera released")

def get_camera():
    """
    Main function to get initialized camera
    """
    cam = CameraModule()
    if cam.initialize():
        return cam
    return None

if __name__ == "__main__":
    # Test camera
    print("=== Testing Camera ===")
    cam = get_camera()
    if cam:
        frame = cam.capture_frame()
        if frame is not None:
            print(f"Frame shape: {frame.shape}")
            cam.capture_photo("test_photo.jpg")
        cam.release()
