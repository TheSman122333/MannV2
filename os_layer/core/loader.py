import os
import importlib

def load_plugins():
    for file in os.listdir("commands"):
        if file.endswith(".py") and file != "__init__.py":
            importlib.import_module(f"commands.{file[:-3]}")
