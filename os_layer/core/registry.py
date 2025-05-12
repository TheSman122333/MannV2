COMMANDS = {}

def register(intent):
    def wrapper(func):
        COMMANDS[intent] = func
        return func
    return wrapper
