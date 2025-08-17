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
import os
from dotenv import load_dotenv
load_dotenv()

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
    
    
from datetime import datetime
from tzlocal import get_localzone

@register("get_time")
def get_time(args):

    local_tz = get_localzone()

    local_time = datetime.now(local_tz)

    formatted_time = local_time.strftime("%I:%M %p, %B %d, %Y")

    return "Local time:" + formatted_time 

@register("get_weather")
def get_weather(args):
    import requests

    location = args.get("location", "Ann Arbor")
    API_KEY =os.getenv("WEATHER_API_KEY")
    BASE_URL = "http://api.weatherapi.com/v1/current.json"

    params = {
        "key": API_KEY,
        "q": location,
        "aqi": "no"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "current" in data:
            temp_f = data["current"]["temp_f"]
            condition = data["current"]["condition"]["text"]
            location_name = data["location"]["name"]
            region = data["location"]["region"]

            return f"Current weather in {location_name}, {region}: {temp_f}°F, {condition}"
        else:
            return "Could not retrieve weather data. Please check the location."
    except Exception as e:
        return f"Error retrieving weather data: {str(e)}"


from ollama import Client

client = Client(host='http://127.0.0.1:11434')

@register("ask_ai")
def ask_ai(args):
    prompt = args.get("prompt")
    model = args.get("model", "llama3")

    if not prompt:
        return "Error: No prompt provided."

    try:
        response = client.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return response.get('message', {}).get('content', 'No response from model.')
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}"
