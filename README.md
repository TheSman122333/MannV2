**MANNV2**

Moderated, Automated, Neural, Network VERSION 2

MANN is a lightweight Python-based voice assistant that brings together automation, AI, and everyday utilities into a single tool.

✨ Features

🎙️ Voice Transcription – Real-time speech-to-text with hotkey control

🌐 Web Search – Open websites or search Google instantly

🖥️ App Control – Launch apps on your system by voice command

🕒 Time & Date – Localized time with timezone detection

☁️ Weather – Live weather info via WeatherAPI

🤖 AI Integration – Chat with local Ollama LLMs

⚡ System Commands – Shutdown or control tasks with a single command

⚙️ Installation

git clone https://github.com/TheSman122333/MannV2.git

cd MannV2

python -m venv venv

source venv/bin/activate   # Linux/Mac

venv\Scripts\activate      # Windows

pip install -r requirements.txt

🔑 Configuration

Add a .env file in the project root:

WEATHER_API_KEY=your_api_key_here


Make sure Ollama is installed and running:

ollama run llama3 (LLAMA3 is default, you can install another, and say ask xyz question to xyz model.)

🚀 Usage

Run the assistant and use commands like:

Speak to the NLU agent, and it will parse your commands via voice, and then send them to be ran and executed.

📦 Dependencies

AppOpener

SpeechRecognition

pyautogui

keyboard

plyer

python-dotenv

tzlocal

requests

ollama

pyttsx3

✨ MANN is your personal AI-powered automation hub, built to simplify life, and save you time.


Made for Summer of Making. (HACK CLUB (originally for neighborhood, but couldn't go))

Contributors: TheSman122333 (swqg-messiah)
