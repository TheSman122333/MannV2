import keyboard
from voice.recognizer import listen
from voice.speaker import say
from nlu.ollama_parser import parse_command
from nlu.create_func import generate_command, generate_command_docs
from core.dispatcher import dispatch
from core.loader import load_plugins
from core.state import recognizer_event

def main():
    load_plugins()
    say("Agent is ready.")
    say("Hold F10 to speak.")
    while True:
        recognizer_event.wait()
        keyboard.wait("f10")
        if not keyboard.is_pressed("f10"):
            continue

        
        text = listen()
        say("Listening...")
        if not text:
            say("Didn't catch that.")
            continue

        result = parse_command(text)
        if result:
            output = dispatch(result["intent"], result.get("args", {}))
            say(output or "Done.")
        else:
            """failed_command = text
            say("Sorry, I didn't understand, but I could try to create this command. Shall I try that?")
            confirmation = listen()
            if any(phrase in confirmation for phrase in ['yes', 'sure', 'go ahead']):
                say("Generating a new command...")
                code = generate_command(failed_command)
                docs = generate_command_docs(failed_command)

                if code and docs:
                    with open("commands/system.py", "a") as f:
                        f.write("\n\n" + code.strip())

                    from nlu.ollama_parser import AVAILABLE_COMMANDS
                    nlu.ollama_parser.AVAILABLE_COMMANDS.append(docs)

                    say("Command generated and documented. Please restart me to activate it.")
                else:
                    say("Failed to generate the command or its documentation.")"""
            say("Did not understand.")

if __name__ == "__main__":
    main()
