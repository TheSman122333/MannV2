from voice.recognizer import listen
from voice.speaker import say
from nlu.ollama_parser import parse_command
from core.dispatcher import dispatch
from core.loader import load_plugins

def main():
    load_plugins()
    say("Agent is ready.")
    while True:
        text = listen()
        if not text:
            say("Didn't catch that.")
            continue
        result = parse_command(text)
        if result:
            output = dispatch(result["intent"], result.get("args", {}))
            say(output or "Done.")
        else:
            say("Sorry, I didn't understand.")

if __name__ == "__main__":
    main()
