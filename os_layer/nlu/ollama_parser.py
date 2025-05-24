from ollama import Client
import json

client = Client(host='http://127.0.0.1:11434')

AVAILABLE_COMMANDS = [
    {
        "intent": "open_app",
        "description": "Open a specific application.",
        "args": { "app": "Name of the application to open." }
    },
    {
        "intent": "search_web",
        "description": "Search something on the web.",
        "args": { "query": "Search string." }
    },
    {
        "intent": "shutdown",
        "description": "Shut down the computer.",
        "args": {}
    },
]

def build_prompt(input_text, commands):
    formatted_cmds = "\n".join([
        f"- intent: {cmd['intent']}\n  description: {cmd['description']}\n  args: {json.dumps(cmd['args'])}"
        for cmd in commands
    ])
    prompt_template = """
You are a desktop assistant. Convert the user request into a command JSON.

Available Commands:
{available_commands}

Examples:
User: "Open calculator"
→ {{ "intent": "open_app", "args": {{ "app": "calculator" }} }}

User: "Lower the volume"
→ {{ "intent": "adjust_volume", "args": {{ "direction": "down" }} }}

Now do this:
User: "{input_text}"
→
"""
    return prompt_template.format(available_commands=formatted_cmds, input_text=input_text)


def parse_command(input_text):
    prompt = build_prompt(input_text, AVAILABLE_COMMANDS)
    response = client.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    content = response['message']['content']
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("Error parsing LLM output:", content)
        return None