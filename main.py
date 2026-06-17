from core.speech_recognition import listen
from core.text_to_speech import speak_hausa
from core.object_detection import detect_objects
from core.ocr_reader import read_text
from core.navigation import get_directions

def main():
    speak_hausa("Barka da rana! Vision-Link AI tana shirye.")
    
    while True:
        command = listen()
        
        if "abubuwa" in command:
            objects = detect_objects()
            speak_hausa(f"Na gano: {objects}")
        
        elif "karatu" in command:
            text = read_text()
            speak_hausa(text)
        
        elif "hanya" in command:
            directions = get_directions()
            speak_hausa(directions)

if __name__ == "__main__":
    main()
