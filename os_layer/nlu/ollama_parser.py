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
    {
        "intent": "transcribe",
        "description": "Toggle voice transcription to type into current window.",
        "args": {
            "action": "Either 'start' or 'stop'."}
    },
    {
        "intent": "ask_wolfram",
        "description": "Ask Wolfram. This command is capable of advanced computations like science and math.",
        "args": {
            "query": "What you want to ask Wolfram"}
    },
    {
        "intent": "get_time",
        "description": "Gets time.",
        "args": {}
    },
    {
        "intent": "get_weather",
        "description": "Gets Weather.",
        "args": {"location": "Location of the weather you want. Defaults to Ann Arbor"}
    },
    {
        "intent": "ask_ai",
        "description": "Asks AI a question.",
        "args": {"prompt": "The question", "model": "Which Ollama model you want to use, by default it is Llama3. DO not put anything here if the user doesn't specify"}
    }



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