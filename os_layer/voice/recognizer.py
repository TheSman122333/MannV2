import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
    try:
        print(r.recognize_google(audio))
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return None  