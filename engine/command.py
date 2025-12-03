import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    # Update the text on the UI
    eel.DisplayMessage(text)
    
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) # 0 for male, 1 for female
    engine.setProperty('rate', 174)
    engine.say(text)
    eel.receiverText(text) # Optional: Pass to chat history if you build one
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage("listening....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage("recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def chat(query):
    # This function handles text input from the UI
    process_command(query)

@eel.expose
def allCommands():
    # This function handles voice input
    query = takecommand()
    print(query)
    
    if query == "":
        eel.ShowHood() # Reset UI if nothing heard
        return

    eel.ShowHood() # Switch back to Hood animation
    process_command(query)

def process_command(query):
    # Common logic for both Voice and Text
    from engine.features import openCommand, setVolume, setBrightness, sendWhatsApp, chatWithBot

    # Clean the query
    query = query.lower()
    
    if "open" in query:
        openCommand(query)
    elif "volume" in query:
        setVolume(query)
    elif "brightness" in query:
        setBrightness(query)
    elif "send message" in query or "whatsapp" in query:
        sendWhatsApp(query)
    else:
        chatWithBot(query)