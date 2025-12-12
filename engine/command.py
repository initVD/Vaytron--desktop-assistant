import speech_recognition as sr
import eel
import time
# IMPORT SPEAK FROM HELPER TO FIX CRASH
from engine.helper import speak 

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        try:
            audio = r.listen(source, 10, 6)
            print('recognizing')
            eel.DisplayMessage('recognizing....')
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")
            eel.DisplayMessage(query)
            time.sleep(2)
        except Exception as e:
            return ""
    
    return query.lower()

@eel.expose
def chat(message):
    # This handles text sent from the UI Chatbox
    process_command(message)

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    
    process_command(query)

def process_command(query):
    try:
        # Import features LOCALLY to avoid circular import errors
        from engine.features import openCommand, PlayYoutube, findContact, whatsApp, makeCall, sendMessage, geminai
        
        query = str(query).lower()

        if "open" in query:
            openCommand(query)
        elif "on youtube" in query:
            PlayYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)

        else:
            geminai(query)
    except Exception as e:
        print(f"Error: {e}")
    
    eel.ShowHood()