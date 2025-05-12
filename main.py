# Python program to translate
# speech to text and text to speech

import ollama
import speech_recognition as sr
import pyttsx3 
from AppOpener import open
from datetime import datetime

# Initialize the recognizer 
r = sr.Recognizer() 

# Function to convert text to
# speech
def SpeakText(command):
    
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()


def get_words_after_first_word_launch(s):
    parts = s.split(' ')
    if 'launch' in s.lower() and len(parts) > 1 or 'open' in s.lower() and len(parts) > 1:
        return ' '.join(parts[1:])  # Return everything after 'launch'
    else:
        return ''  # Return an empty string if 'launch' is not present
    

def get_words_after_first_word_launch_askai(s):
    parts = s.split(' ')
    if 'ask' or 'what' or 'when' or 'how' or 'why' in s.lower() and len(parts) > 1:
        return ' '.join(parts[1:])  # Return everything after the first word
    else:
        return ''

# Loop infinitely for user to
# speak

modelfile='''
FROM openchat
SYSTEM You are an AI named openchat. Your only job is to cover up and make the speech to text module look good. If it messes up and cuts out some words, take the most logical approach and fill in that word. Basically, just assume.
'''
ollama.create(model='openchat-mod', modelfile=modelfile)



while(1):    
    
    # Exception handling to handle
    # exceptions at the runtime
    try:
        
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source2, duration=0.4)
            
            #listens for the user's input 
            audio2 = r.listen(source2)
            
            # Using google to recognize audio
            SpokenText = r.recognize_google(audio2)
            SpokenText = SpokenText.lower()

            print(f"Did you say: {SpokenText}?")

            appToOpen = get_words_after_first_word_launch(SpokenText)
            prompt = get_words_after_first_word_launch_askai(SpokenText)

            if appToOpen != '':
                try:
                    open(appToOpen, match_closest=True, throw_error=True)
                except Exception as e:
                    print(f"App '{appToOpen}' not found. Error: {str(e)}")
                    SpeakText(f'{appToOpen} not found. Please try again.')
            elif prompt != '':
                try:
                    if 'what' and 'time' and 'is' and 'it' in prompt:
                        SpeakText(datetime.now().strftime('%H:%M:%S'))
                    else:
                        response = ollama.chat(model='openchat-mod', messages=[
                        {
                            'role': 'user',
                            'content': prompt,
                        },
                        ])
                        SpeakText(response['message']['content'])
                except:
                    SpeakText("There was an error. Please try again.")

    except sr.UnknownValueError:
        print("unknown error occurred")