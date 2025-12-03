import os
import re
import eel
import pyautogui
import screen_brightness_control as sbc
from AppOpener import open as appopen
from playsound import playsound
import google.generativeai as genai
from engine.config import ASSISTANT_NAME, GEMINI_API_KEY
from engine.command import speak

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')
chat_session = model.start_chat(history=[])

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\bootup.mp3"
    playsound(music_dir)

def openCommand(query):
    for name in ASSISTANT_NAME:
        query = query.replace(name, "")
    query = query.replace("open", "").replace("launch", "").strip().lower()

    if query != "":
        speak("Opening " + query)
        try:
            appopen(query, match_closest=True, throw_error=True)
        except:
            os.system('start ' + query)
    else:
        speak("Please specify what to open")

def setVolume(command):
    if "up" in command or "increase" in command:
        pyautogui.press("volumeup")
        speak("Volume increased")
    elif "down" in command or "decrease" in command:
        pyautogui.press("volumedown")
        speak("Volume decreased")
    elif "mute" in command:
        pyautogui.press("volumemute")
        speak("System muted")

def setBrightness(command):
    current = sbc.get_brightness()
    if not current: current = [50]
    
    if "up" in command or "increase" in command:
        sbc.set_brightness(min(current[0] + 10, 100))
        speak("Brightness increased")
    elif "down" in command or "decrease" in command:
        sbc.set_brightness(max(current[0] - 10, 0))
        speak("Brightness decreased")

def sendWhatsApp(query):
    import pywhatkit
    # Add your contacts here
    contacts = {"mom": "+919725338658", "dad": "+919925826289"}
    
    for name, number in contacts.items():
        if name in query:
            msg = query.replace("send message to", "").replace(name, "").replace("saying", "").strip()
            speak(f"Sending message to {name}")
            pywhatkit.sendwhatmsg_instantly(number, msg, wait_time=10)
            return
    speak("I couldn't find that contact.")

def chatWithBot(query):
    try:
        eel.DisplayMessage("Thinking...")
        prompt = f"You are Vaytron, a desktop assistant. Answer this query simply and concisely: {query}"
        response = chat_session.send_message(prompt)
        answer = response.text.replace("*", "")
        speak(answer)
    except Exception as e:
        print(f"Error: {e}")
        speak("I am having trouble connecting to the internet.")