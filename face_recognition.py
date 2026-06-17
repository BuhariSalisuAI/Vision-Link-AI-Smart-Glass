# face_recognition.py
# Vision-Link AI Smart Glass - Face Recognition Module
# Detects and recognizes faces

import cv2
import numpy as np
import pickle
import os
import config
from TTS import speak_hausa

class FaceRecognition:
    def __init__(self):
        self.known_faces = {}
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.known_faces_file = 'app/models/known_faces.pkl'
        
        # Load known faces if available
        self.load_known_faces()
    
    def load_known_faces(self):
        """
        Load previously saved face data
        """
        if os.path.exists(self.known_faces_file):
            with open(self.known_faces_file, 'rb') as f:
                data = pickle.load(f)
                self.known_faces = data['names']
                self.recognizer.read(data['model_path'])
            print(f"Loaded {len(self.known_faces)} known faces.")
    
    def detect_faces(self, image):
        """
        Detect faces in an image
        Returns: list of face rectangles (x, y, w, h)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces
    
    def recognize_face(self, image, face_rect):
        """
        Recognize a detected face
        Returns: str (person's name or "Unknown")
        """
        x, y, w, h = face_rect
        face_roi = image[y:y+h, x:x+w]
        gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        
        try:
            # Try to recognize
            label, confidence = self.recognizer.predict(gray_face)
            
            if confidence < 100:  # Lower is better for LBPH
                name = self.known_faces.get(label, "Unknown")
                return name, confidence
            else:
                return "Unknown", confidence
                
        except:
            return "Unknown", 999
    
    def add_new_face(self, image, name, num_samples=10):
        """
        Add a new person to the database
        Args:
            image: First image of the person
            name: Person's name
            num_samples: Number of photos to capture
        """
        speak_hausa(f"Na shirya karbar hotunan {name}. Ka duba kyamara.")
        
        faces_data = []
        labels = []
        current_id = len(self.known_faces)
        
        # Capture multiple samples
        for i in range(num_samples):
            faces = self.detect_faces(image)
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_roi = cv2.cvtColor(image[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
                faces_data.append(face_roi)
                labels.append(current_id)
                
                speak_hausa(f"Hoton {i+1} na {num_samples}")
                
                # Small delay between captures
                import time
                time.sleep(0.5)
        
        if faces_data:
            # Train recognizer
            self.recognizer.update(faces_data, np.array(labels))
            self.known_faces[current_id] = name
            
            # Save to file
            self.save_known_faces()
            speak_hausa(f"An ajiye {name} cikin database.")
            return True
        
        speak_hausa("Ba na iya gano fuska. Sake gwadawa.")
        return False
    
    def save_known_faces(self):
        """
        Save face database to file
        """
        model_path = 'app/models/face_recognizer.yml'
        self.recognizer.write(model_path)
        
        data = {
            'names': self.known_faces,
            'model_path': model_path
        }
        
        with open(self.known_faces_file, 'wb') as f:
            pickle.dump(data, f)
    
    def identify_people(self, image):
        """
        Main function: Detect and identify all faces in image
        Returns: list of (name, confidence) tuples
        """
        faces = self.detect_faces(image)
        results = []
        
        if len(faces) == 0:
            speak_hausa("Babu fuska a gaban ku.")
            return []
        
        speak_hausa(f"Na gano fuska {len(faces)}.")
        
        for face in faces:
            name, confidence = self.recognize_face(image, face)
            results.append((name, confidence))
            
            if name != "Unknown":
                speak_hausa(f"Wannan {name} ne.")
            else:
                speak_hausa("Wannan mutumin ba na san shi ba.")
        
        return results

def recognize_faces_in_image(image):
    """
    Main function to call face recognition
    """
    face_rec = FaceRecognition()
    return face_rec.identify_people(image)

def add_person(image, name):
    """
    Add a new person to the database
    """
    face_rec = FaceRecognition()
    return face_rec.add_new_face(image, name)

if __name__ == "__main__":
    # Test face recognition
    print("=== Testing Face Recognition ===")
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            recognize_faces_in_image(frame)
        cap.release()
