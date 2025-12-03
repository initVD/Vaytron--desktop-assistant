import os
import re
import eel
import pyautogui
import screen_brightness_control as sbc
from AppOpener import open as appopen
from playsound import playsound
from engine.config import ASSISTANT_NAME
from command import speak


# --- SYSTEM CONTROLS --- #

def setVolume(command):
    if "up" in command or "increase" in command:
        pyautogui.press("volumeup")
        speak("Volume increased")
    elif "dowm" in command or "decrease" in command:
        pyautogui.press("volumedown")
        speak("Volume decreased")
    elif "mute" in command:
        pyautogui.press("volumemute")
        speak("System muted")

def setBrightness(command):
    current = sbc.get_brightness()
    if not current:
        current = [50]#default

    if "up" in command or "increase" in command:
        sbc.set_brightness(min(current[0]+10,100))
        speak("Brightness increased")
    elif "down" in command or "decrease" in command:
        sbc.set_brightness(max(current[0]-10,0))
        speak("Brightness decreased")



    

#playing assistannt sound function
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\bootup.mp3"
    playsound(music_dir)
    
def openCommand(query):
    # Clean the query (remove "open", "jarvis", etc.)
    for name in ASSISTANT_NAME:
        query = query.replace(name, "")
    query = query.replace("open", "").replace("launch", "").strip().lower()

    if query != "":
        speak("Opening " + query)
        try:
            # Try generic app opener first
            appopen(query, match_closest=True, throw_error=True)
        except:
            # Fallback to system start command if AppOpener fails
            os.system('start ' + query)
    else:
        speak("Please specify what to open")

def chatWithBot(query):
    speak("I heard you say: " + query)

def sendWhatsApp(query):
    import pywhatkit

    contact = {
        "mom": "+919725338658",
        "dad": "+919925826289",
        "sister":"+919924083240"
    }
    for name, number in contact.items():
        if name in query