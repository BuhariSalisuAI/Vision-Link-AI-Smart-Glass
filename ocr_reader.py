# ocr_reader.py
# Vision-Link AI Smart Glass - OCR (Optical Character Recognition)
# Reads text from images using Tesseract OCR

import cv2
import pytesseract
import numpy as np
import config
from TTS import print

class OCRReader:
    def __init__(self):
        # Path to Tesseract executable (for Raspberry Pi)
        # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        self.language = 'eng+ha'  # English + Hausa
        
    def preprocess_image(self, image):
        """
        Preprocess image for better OCR accuracy
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        return denoised
    
    def read_text(self, image_path=None, camera=None):
        """
        Read text from image or camera
        Args:
            image_path: Path to image file (optional)
            camera: Camera object for live capture (optional)
        Returns: str (detected text)
        """
        # Get image
        if image_path:
            image = cv2.imread(image_path)
        elif camera:
            ret, image = camera.read()
            if not ret:
                print("Ba na iya karɓar hoto daga kyamara.")
                return None
        else:
            print("Babu hoto don karatu.")
            return None
        
        # Preprocess
        processed = self.preprocess_image(image)
        
        # Perform OCR
        try:
            text = pytesseract.image_to_string(
                processed, 
                lang=self.language,
                config='--psm 6'  # Assume uniform block of text
            )
            
            # Clean up text
            text = text.strip()
            text = ' '.join(text.split())  # Remove extra spaces
            
            if text:
                print(f"OCR Result: {text}")
                return text
            else:
                print(config.HAUSA_PHRASES['no_text'])
                return None
                
        except Exception as e:
            print(f"OCR Error: {e}")
            print("Akwai matsala wajen karatu rubutu.")
            return None
    
    def read_text_live(self, camera, duration=3):
        """
        Read text from live camera feed for specified duration
        """
        print("Ina karatu rubutu. Ka tsaya da kyamara a kan rubutu.")
        
        import time
        start_time = time.time()
        best_text = ""
        
        while time.time() - start_time < duration:
            ret, frame = camera.read()
            if ret:
                text = pytesseract.image_to_string(
                    self.preprocess_image(frame),
                    lang=self.language
                )
                if len(text.strip()) > len(best_text):
                    best_text = text.strip()
        
        if best_text:
            print(f"Na gano rubutu: {best_text}")
            return best_text
        else:
            print("Babu rubutu da na iya karatu.")
            return None

def read_text_from_camera(camera):
    """
    Main function to call OCR
    """
    ocr = OCRReader()
    text = ocr.read_text_live(camera)
    return text

if __name__ == "__main__":
    # Test with sample image or camera
    print("=== Testing OCR ===")
    # Test with camera
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        result = read_text_from_camera(cap)
        print(f"Result: {result}")
        cap.release()
    else:
        print("Camera not available")
