import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)    # Speed
engine.setProperty('volume', 1.0)  # Volume

def speak(text):
    print(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

# Test karo
speak("Hello! I am your AI Assistant. I can recognize your face and detect your emotions.")