import os
import re
import eel
import pyautogui
import screen_brightness_control as sbc
from AppOpener import open as appopen
import pywhatkit
import google.generativeai as genai
from engine.config import ASSISTANT_NAME, GEMINI_API_KEY

# Gemini Configuration
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Persistent Chat Memory
system_instruction = "You are Vaytron, a desktop assistant. Answer properly, short and concisely."
chat_session = model.start_chat(history=[
    {"role": "user", "parts": [system_instruction]},
    {"role": "model", "parts": ["Okay, I am Vaytron."]}
])

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").replace("launch", "").strip().lower()
    if query != "":
        from engine.command import speak 
        speak("Opening " + query)
        try:
            appopen(query, match_closest=True, throw_error=True)
        except:
            os.system('start ' + query)

def setVolume(command):
    from engine.command import speak
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
    from engine.command import speak
    current = sbc.get_brightness()
    if not current: current = [50]
    
    if "up" in command or "increase" in command:
        sbc.set_brightness(min(current[0] + 10, 100))
        speak("Brightness increased")
    elif "down" in command or "decrease" in command:
        sbc.set_brightness(max(current[0] - 10, 0))
        speak("Brightness decreased")

def sendWhatsApp(query):
    from engine.command import speak
    # TODO: Update these numbers with real contacts
    contacts = {"mom": "+910000000000", "dad": "+910000000000"} 
    
    for name, number in contacts.items():
        if name in query:
            msg = query.replace("send message to", "").replace(name, "").replace("saying", "").strip()
            speak(f"Sending message to {name}")
            # Sends message instantly
            pywhatkit.sendwhatmsg_instantly(number, msg, wait_time=10)
            return
    speak("I couldn't find that contact.")

def chatWithBot(query):
    from engine.command import speak
    try:
        eel.DisplayMessage("Thinking...")
        response = chat_session.send_message(query)
        answer = response.text.replace("*", "")
        
        eel.DisplayMessage("Speaking...")
        speak(answer)
    except Exception as e:
        print(f"Error: {e}")
        speak("I am having trouble connecting to the internet.")