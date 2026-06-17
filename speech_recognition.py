# speech_recognition.py
# Vision-Link AI Smart Glass - Speech Recognition Module
# Converts speech to text (Hausa & English)

import speech_recognition as sr
import config
from TTS import speak_hausa

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            print("Saita microphone...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Microphone shirya.")
    
    def listen(self, timeout=5):
        """
        Listen to microphone and convert speech to text
        Returns: str (recognized text) or None
        """
        with self.microphone as source:
            print("Ina saurara... (Ina jira magana)")
            speak_hausa("Ina saurara.")
            
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                print("Na karɓi magana. Ina fassara...")
                
                # Try Hausa first, then English
                try:
                    text = self.recognizer.recognize_google(audio, language='ha-NG')
                    print(f"An gano (Hausa): {text}")
                    return text.lower()
                except:
                    text = self.recognizer.recognize_google(audio, language='en-US')
                    print(f"An gano (English): {text}")
                    return text.lower()
                    
            except sr.WaitTimeoutError:
                print("Babu magana da aka ji.")
                speak_hausa("Babu magana da na ji. Sake faɗa.")
                return None
                
            except sr.UnknownValueError:
                print("Ba na fahimtar maganar.")
                speak_hausa("Ba na fahimtar maganar. Sake faɗa.")
                return None
                
            except sr.RequestError as e:
                print(f"Error: {e}")
                speak_hausa("Akwai matsala da intanet.")
                return None

def listen_for_command():
    """
    Main function to listen for user commands
    """
    recognizer = SpeechRecognizer()
    
    # Common command keywords in Hausa and English
    commands = {
        'abubuwa': 'detect_objects',
        'objects': 'detect_objects',
        'karatu': 'read_text',
        'read': 'read_text',
        'rubutu': 'read_text',
        'hanya': 'navigation',
        'direction': 'navigation',
        'navigation': 'navigation',
        'gida': 'navigation',
        'taimako': 'emergency',
        'help': 'emergency',
        'gaggawa': 'emergency',
        'emergency': 'emergency',
        'fuska': 'face_recognition',
        'face': 'face_recognition',
        'wani ne': 'face_recognition',
        'who': 'face_recognition',
    }
    
    text = recognizer.listen()
    
    if text:
        # Check for command keywords
        for keyword, action in commands.items():
            if keyword in text:
                return action
        
        # If no command found
        speak_hausa("Ba na fahimtar umarnin. Sake faɗa ko amfani da button.")
        return None
    
    return None

if __name__ == "__main__":
    # Test the speech recognition
    print("=== Testing Speech Recognition ===")
    while True:
        result = listen_for_command()
        if result:
            print(f"Command detected: {result}")
            break
