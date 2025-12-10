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

# Initialize Chat with System Instruction
system_instruction = (
    "You are Vaytron, a desktop assistant. "
    "Answer properly, short, and concisely. "
    "ALWAYS detect the language of the user's input and respond strictly in that same language. "
    "If the user speaks Hindi, answer in Hindi. If English, answer in English."
)

chat_session = model.start_chat(history=[
    {"role": "user", "parts": [system_instruction]},
    {"role": "model", "parts": ["Okay, I am Vaytron. I will answer in the language ,you speaks."]}
])
def openCommand(query):
    # Fix: Handle both List and String for Assistant Name
    query = query.lower()
    
    if isinstance(ASSISTANT_NAME, list):
        for name in ASSISTANT_NAME:
            query = query.replace(name.lower(), "")
    else:
        query = query.replace(ASSISTANT_NAME.lower(), "")

    query = query.replace("open", "").replace("launch", "").strip()
    
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
    # Update these numbers with real contacts
    contacts = {"mom": "+910000000000", "dad": "+910000000000"} 
    
    for name, number in contacts.items():
        if name in query:
            msg = query.replace("send message to", "").replace(name, "").replace("saying", "").strip()
            speak(f"Sending message to {name}")
            pywhatkit.sendwhatmsg_instantly(number, msg, wait_time=10)
            return
    speak("I couldn't find that contact.")

def chatWithBot(query):
    from engine.command import speak
    try:
        eel.DisplayMessage("Thinking...")
        
        # The AI will now generate the answer in the correct language
        response = chat_session.send_message(query)
        answer = response.text.replace("*", "")
        
        eel.DisplayMessage("Speaking...")
        speak(answer)
    except Exception as e:
        print(f"Error: {e}")
        speak("I am having trouble connecting to the internet.")