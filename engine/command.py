import speech_recognition as sr
import eel
import time
import re
from engine.voice import speak_realistic

def speak(text):
    eel.DisplayMessage(text)
    # eel.receiverText(text) 
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
    if not query: return
    process_command(query)

@eel.expose
def allCommands():
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
    # Import features
    from engine.features import (openCommand, setVolume, setBrightness, sendWhatsApp, 
                                 system_stats, check_password_safety, 
                                 research_topic, open_social_media, chatWithBot)
    
    query = query.lower()
    print(f"Processing: {query}")
    
    # --- Advanced Commands ---
    if "system status" in query or "battery" in query: system_stats()
    elif "check password" in query: check_password_safety(query.replace("check password", "").strip())
    elif "research" in query: research_topic(query.replace("research", "").strip())
    elif "open twitter" in query: open_social_media("twitter")
    
    # --- Basic Commands (Added these back!) ---
    elif "open" in query: openCommand(query)
    elif "volume" in query: setVolume(query)
    elif "brightness" in query: setBrightness(query)
    elif "send message" in query or "whatsapp" in query: sendWhatsApp(query)
    
    # --- Chat (AI) ---
    else: chatWithBot(query)