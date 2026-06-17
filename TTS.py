import pyttsx3

def speak_hausa(text):
    engine = pyttsx3.init()
    # Saita muryar Hausa (idana akwai)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
