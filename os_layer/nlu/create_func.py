from ollama import Client
import json
import re

client = Client(host='http://127.0.0.1:11434')

def generate_command(input_text):
    response = client.chat(model="mistral", messages=[{"role": "user", "content": """You are a Python code generation assistant.

Generate a new command function following this structure:

@register("command_name")
def command_name(args):
    # Extract and validate parameters from args
    # Attempt to perform the action
    # Return a string describing the result

Example:

@register("open_app")
def open_app(args):
    app = args.get("app", "")
    if not app:
        return "App name missing."

    try:
        open(app, match_closest=True, throw_error=True)
        return f"Opening {{app}}..."
    except Exception as e:
        return f"Failed to open '{{app}}': {{str(e)}}'

Now, generate a command based on this: "{}". DO NOT WRITE ANYTHING EXTRA. ONLY CODE. 
""".format(input_text)}])
    content = response['message']['content']
    try:
        print(content)
        return content
    except json.JSONDecodeError:
        print("Error parsing LLM output:", content)
        return None
    
def generate_command_docs(input_text):
    prompt = f"""
You are a documentation assistant for an AI agent.

Based on the user request: "{input_text}", generate a JSON documentation entry
for an AVAILABLE_COMMANDS list, in this format:

{{
  "intent": "intent_name",
  "description": "What the command does",
  "args": {{
    "arg_name": "description of argument"
  }}
}}

Only return valid JSON. DO NOT WRITE ANYTHING EXTRA. ONLY CODE
"""
    response = client.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    content = response['message']['content']
    try:
        print(content)
        return json.loads(content)
    except json.JSONDecodeError:
        print("Error parsing doc output:", content)
        return None
