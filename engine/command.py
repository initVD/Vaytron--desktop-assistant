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
            # Listen for max 10 seconds, timeout if silence
            audio = r.listen(source, 10, 6)
            eel.DisplayMessage("recognizing....")
            query = r.recognize_google(audio, language='en-in')
            eel.DisplayMessage(query)
        except Exception as e:
            return ""
    return query.lower()

@eel.expose
def chat(query):
    query = query.lower()
    # Check for text-based stop commands
    if query in ["stop", "exit", "quit", "bye"]:
        speak("Going to sleep, sir.")
        eel.ShowHood()
        return
    process_command(query)

@eel.expose
def allCommands():
    try:
        # Greeting command handled by main.js, but we start loop here
        while True:
            query = takecommand()
            
            if query == "":
                continue

            # Check for voice-based stop commands
            if "stop" in query or "exit" in query or "quit" in query:
                speak("Going to sleep, sir.")
                eel.ShowHood()
                break

            eel.DisplayMessage("Processing...")
            process_command(query)
            
            # Tiny sleep to ensure audio doesn't overlap
            time.sleep(1) 
            eel.DisplayMessage("Listening again...")
            
    except Exception as e:
        print(f"Error: {e}")
        eel.ShowHood()

def process_command(query):
    from engine.features import openCommand, setVolume, setBrightness, sendWhatsApp, chatWithBot
    
    query = query.lower()
    # Split multi-commands (e.g., "Open google and youtube")
    commands = re.split(r'\s+(?:and|also|then)\s+', query)
    
    for command in commands:
        if not command.strip(): continue
        # Ignoring stop words if they appear in middle of sentence
        if command in ["stop", "exit", "quit"]: continue

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