import os
import re
import eel
import pyautogui
import screen_brightness_control as sbc
from AppOpener import open as appopen
from playsound import playsound
from engine.config import ASSISTANT_NAME, GEMINI_API_KEY
from command import speak
import google.generativeai as genai

# --- CONFIGURING GEMINI --- #
# We authenticate with Google using the key from config.py
genai.configure(api_key=GEMINI_API_KEY)

# We define the model (Gemini-1.5-flash is fast and good for chat)
model = genai.GenerativeModel("gemini-1.5-flash")

# This is the memory of the conversation
chat_session = model.start_chat(history=[])

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\bootup.mp3"
    playsound(music_dir)


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
    try:
        #giving prompt to model
        prompt:f"You are Vaytron, a smart and friendly desktop assistant. Detect the user's language automatically and reply in the same language. Give simple, clear, and concise answers (preferably within 1–2 sentences). Keep your tone helpful and easy to understand for all users.: {query}"

        #sending message to gemini
        response = chat_session.send_message(prompt)

        # 3. Get the text answer
        answer = response.text

        # 4. Clean up the answer
            # (Remove * asterisks which AI uses for bolding, but TTS reads annoyingly)'
        answer = answer.replace("*", "")
        
        speak(answer)
    except Exception as e:
        print(f"Error: {e}")
        speak("I had trouble connecting to my brain. Please check your internet.")


def sendWhatsApp(query):
    import pywhatkit

    contact = {
        "mom": "+919725338658",
        "dad": "+919925826289", 
        "sister":"+919924083240"
    }
    for name, number in contact.items():
        if name in query:
            msg = query.replace("send message to ", "").replace("saying","").strip()
            speak(f"Sending WhatsApp message to {name}")
            # This will open WhatsApp Web and send the message
            pywhatkit.sendingwhatmsg_instantly(number,msg, wait_time=10)
            return
    speak("Contact not found in your contact list")
