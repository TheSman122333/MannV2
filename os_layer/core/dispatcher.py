from core.registry import COMMANDS

def dispatch(intent, args):
    if intent in COMMANDS:
        return COMMANDS[intent](args)
    else:
        return f"Unknown command: {intent}"
