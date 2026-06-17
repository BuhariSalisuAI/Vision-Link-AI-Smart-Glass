# test_speech.py
# Vision-Link AI Smart Glass - Test Speech Module

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.speech_recognition import listen_for_command
from app.TTS import speak_hausa

def test_text_to_speech():
    """
    Test TTS functionality
    """
    print("=== Testing Text-to-Speech ===")
    
    test_phrases = [
        "Barka da rana!",
        "Vision-Link AI tana shirye.",
        "Na gano mutum a gaban ku.",
        "Koma hagu.",
        "Kun isa wurin ku.",
    ]
    
    for phrase in test_phrases:
        print(f"Speaking: {phrase}")
        speak_hausa(phrase)
    
    print("TTS test completed.")

def test_speech_to_text():
    """
    Test STT functionality
    """
    print("\n=== Testing Speech-to-Text ===")
    print("Please say a command...")
    
    result = listen_for_command()
    
    if result:
        print(f"Command recognized: {result}")
    else:
        print("No command recognized.")

def test_hausa_phrases():
    """
    Test all Hausa phrases
    """
    print("\n=== Testing Hausa Phrases ===")
    
    from app.config import HAUSA_PHRASES
    
    for key, phrase in HAUSA_PHRASES.items():
        print(f"Testing phrase '{key}': {phrase}")
        speak_hausa(phrase)

if __name__ == "__main__":
    print("Vision-Link AI - Speech Module Tests")
    print("=" * 40)
    
    # Run all tests
    test_text_to_speech()
    test_speech_to_text()
    test_hausa_phrases()
    
    print("\nAll tests completed!")
