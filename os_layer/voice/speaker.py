import pyttsx3

engine = pyttsx3.init()

def say(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()
