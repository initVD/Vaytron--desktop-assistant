import speech_recognition as sr
import eel
import time
import re
from engine.voice import speak_realistic

def speak(text):
    eel.DisplayMessage(text)
    # eel.receiverText(text) # Commented out to prevent JS errors if not defined
    speak_realistic(text)

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        eel.DisplayMessage("listening....")
        r.pause_threshold = 0.5 
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, 10, 6)
            eel.DisplayMessage("recognizing....")
            query = r.recognize_google(audio, language='en-in')
            eel.DisplayMessage(query)
        except:
            return ""
    return query.lower()

@eel.expose
def chat(query):
    # This handles TEXT input from the chatbox
    if not query: return
    process_command(query)

@eel.expose
def allCommands():
    # This handles VOICE input loop
    try:
        while True:
            query = takecommand()
            if not query: continue
            if "stop" in query or "exit" in query:
                speak("Goodbye.")
                eel.ShowHood()
                break
            process_command(query)
            time.sleep(1)
    except:
        eel.ShowHood()

def process_command(query):
    from engine.features import (openCommand, system_stats, check_password_safety, 
                                 research_topic, open_social_media, chatWithBot)
    
    query = query.lower()
    print(f"Processing: {query}") # Debug print
    
    if "system status" in query or "battery" in query: system_stats()
    elif "check password" in query: check_password_safety(query.replace("check password", "").strip())
    elif "research" in query: research_topic(query.replace("research", "").strip())
    elif "open twitter" in query: open_social_media("twitter")
    elif "open" in query: openCommand(query)
    else: chatWithBot(query)