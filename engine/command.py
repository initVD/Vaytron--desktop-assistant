import speech_recognition as sr
import eel
import time
import re

from engine.voice import speak_realistic

def speak(text):
    eel.DisplayMessage(text)
    eel.receiverText(text)
    speak_realistic(text)

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        eel.DisplayMessage("listening....")
        r.pause_threshold = 0.5 
        r.adjust_for_ambient_noise(source)
        try:
            # Wait max 10 seconds for a phrase, else return empty
            audio = r.listen(source, 10, 5) 
            eel.DisplayMessage("recognizing....")
            query = r.recognize_google(audio, language='en-in')
            eel.DisplayMessage(query)
        except Exception as e:
            return ""
    return query.lower()

@eel.expose
def chat(query):
    process_command(query)

@eel.expose
def allCommands():
    try:
        # Initial greeting
        # speak("I am listening, sir.") # Optional
        
        # MAX_SILENCE_COUNT determines how many times it listens to silence before sleeping
        silence_count = 0
        MAX_SILENCE = 2 

        while True:
            query = takecommand()
            
            if query == "":
                silence_count += 1
                if silence_count > MAX_SILENCE:
                    speak("Going to sleep now.")
                    eel.ShowHood()
                    break # Exit the loop
                continue
            
            # Reset silence count if user spoke
            silence_count = 0 

            if "stop" in query or "exit" in query or "quit" in query:
                speak("Goodbye, sir.")
                eel.ShowHood()
                break

            eel.DisplayMessage("Processing...")
            process_command(query)
            
            # Important: Small delay to ensure audio output doesn't trigger input
            time.sleep(1) 
            eel.DisplayMessage("Listening again...")

    except Exception as e:
        print(f"Error: {e}")
        eel.ShowHood()

def process_command(query):
    from engine.features import openCommand, setVolume, setBrightness, sendWhatsApp, chatWithBot
    
    query = query.lower()
    commands = re.split(r'\s+(?:and|also|then)\s+', query)
    
    for command in commands:
        if not command.strip(): continue

        if "open" in command:
            openCommand(command)
        elif "volume" in command:
            setVolume(command)
        elif "brightness" in command:
            setBrightness(command)
        elif "send message" in command or "whatsapp" in command:
            sendWhatsApp(command)
        else:
            chatWithBot(command)