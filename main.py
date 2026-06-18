from speech_recognition import listen_for_command
from text_to_speech import speak_hausa
from object_detection import detect_objects
from ocr_reader import read_text
from navigation import get_directions

def main():
    speak_hausa("Barka da rana! Vision-Link AI tana shirye.")
    
    while True:
        command = listen_for_command()
        
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
