import keyboard
from voice.recognizer import listen
from voice.speaker import say
from nlu.ollama_parser import parse_command
from core.dispatcher import dispatch
from core.loader import load_plugins
from core.state import recognizer_event
import os
from dotenv import load_dotenv

def main():
    load_plugins()
    say("Agent is ready.")
    say("Hold F10 to speak.")
    while True:
        recognizer_event.wait()
        keyboard.wait("f10")
        if not keyboard.is_pressed("f10"):
            continue

        say("Listening...")
        text = listen()
        if not text:
            say("Didn't catch that.")
            continue

        result = parse_command(text)
        if result:
            output = dispatch(result["intent"], result.get("args", {}))
            say(output or "Done.")
        else:
            say("Did not understand.")

if __name__ == "__main__":
    main()
