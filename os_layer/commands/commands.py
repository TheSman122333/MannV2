from AppOpener import open
from core.registry import register
import os
import webbrowser
import re
import threading
import speech_recognition as sr
import pyautogui
import time
from core.state import recognizer_event
import keyboard
from voice.speaker import say
from plyer import notification

stop_transcription_flag = False


@register("open_app")
def open_app(args):
    app = args.get("app", "")
    if not app:
        return "App name missing."

    try:
        open(app, match_closest=True, throw_error=True)
        return f"Opening {app}..."
    except Exception as e:
        return f"Failed to open '{app}': {str(e)}"

@register("search_web")
def search_web(args):
    query = args.get("query", "")
    if not query:
        return "Search query is missing."


    url_pattern = re.compile(
        r'^(https?:\/\/)?'             
        r'([\da-z\.-]+)\.([a-z\.]{2,6})'
        r'([\/\w \.-]*)*\/?$'          
    )


    if url_pattern.match(query):
        if not query.startswith("http://") and not query.startswith("https://"):
            query = "http://" + query 
        try:
            webbrowser.open(query)
            return f"Opening link: {query}"
        except Exception as e:
            return f"Failed to open link '{query}': {str(e)}"
    else:
    
        search_url = f"https://www.google.com/search?q={query}"
        try:
            webbrowser.open(search_url)
            return f"Searching the web for: {query}"
        except Exception as e:
            return f"Failed to search for '{query}': {str(e)}"
        

@register("shutdown")
def shutdown(args):
    
    try:
        if os.name == 'nt': 
            os.system("shutdown /s /f /t 0")
        else: 
            os.system("shutdown -h now")
        return "Shutting down the system..."
    except Exception as e:
        return f"Failed to shutdown: {str(e)}"
    

listening = False
listener_thread = None

def on_stop_hotkey():
    global stop_transcription_flag
    stop_transcription_flag = True
    print("Manual stop key pressed.")
    

def transcription_loop():
    global listening, stop_transcription_flag
    from core.state import recognizer_event

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    stop_transcription_flag = False
    print("Transcription is now active. Press Ctrl+Shift+D to stop.")
    
    try:
        while listening and not stop_transcription_flag:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print(f"Transcribed: {text}")
                pyautogui.write(text + " ")
                time.sleep(0.2)
            except sr.UnknownValueError:
                print("Could not understand.")
            except sr.RequestError as e:
                print(f"Speech API error: {e}")
            except Exception as e:
                print(f"Transcription error: {e}")

    finally:
        listening = False
        recognizer_event.set()
        keyboard.remove_hotkey(stop_hotkey_handle)
        print("Transcription ended, main recognizer resumed.")
        notification.notify(
            title="Transcription",
            message="Transcription ended.",
            timeout=3
        )

@register("transcribe")
def transcribe(args):
    global listening, listener_thread, stop_hotkey_handle
    action = args.get("action", "").lower()

    if action == "start":
        listening = True
        stop_hotkey_handle = keyboard.add_hotkey("ctrl+shift+d", on_stop_hotkey)
        recognizer_event.clear()
        listener_thread = threading.Thread(target=transcription_loop, daemon=True)
        listener_thread.start()
        notification.notify(
            title="Transcription",
            message="Transcription started. Press Ctrl+Shift+D to stop.",
            timeout=3
        )
        return "Transcription started. Press Ctrl+Shift+D to stop manually."


    elif action == "stop":
        if not listening:
            return "Transcription is not running."
        listening = False
        recognizer_event.set()
        keyboard.remove_hotkey(stop_hotkey_handle)
        return "Transcription stopped."
    else:
        return "Invalid action. Use 'start' or 'stop'."