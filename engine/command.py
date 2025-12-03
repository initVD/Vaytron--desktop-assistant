import speech_recognition as sr
import eel
import time
from engine.voice import speak_realistic

def speak(text):
    eel.DisplayMessage(text)
    eel.receiverText(text)
    speak_realistic(text)

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage("listening....")
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, 10, 5)
            print('recognizing')
            eel.DisplayMessage("recognizing....")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")
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
        # Start the continuous loop
        while True:
            # 1. Listen for input
            query = takecommand()
            
            # 2. Handle Silence (If user didn't speak, keep listening)
            if query == "":
                continue

            # 3. EXIT CONDITION: Check if user wants to stop
            if "stop" in query or "exit" in query or "quit" in query:
                from engine.features import speak
                speak("Going to sleep, sir.")
                eel.ShowHood()  # This switches the UI back to the Circle/Hood
                break # Breaks the loop

            # 4. If not stopping, process the command(s)
            eel.DisplayMessage("Processing...")
            process_command(query)
            
            # 5. Ready for next command
            eel.DisplayMessage("Listening again...")

    except Exception as e:
        print(f"Error in main loop: {e}")
        eel.ShowHood()

def process_command(query):
    # Import inside function to prevent circular import error
    from engine.features import openCommand, setVolume, setBrightness, sendWhatsApp, chatWithBot
    
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