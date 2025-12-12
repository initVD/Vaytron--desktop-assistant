import os
import re
import time
import markdown2
from bs4 import BeautifulSoup
import pyttsx3
import eel

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None

def remove_words(input_string, words_to_remove):
    words = input_string.split()
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    result_string = ' '.join(filtered_words)
    return result_string

def keyEvent(key_code):
    command =  f'adb shell input keyevent {key_code}'
    os.system(command)
    time.sleep(1)

def tapEvents(x, y):
    command =  f'adb shell input tap {x} {y}'
    os.system(command)
    time.sleep(1)

def adbInput(message):
    command =  f'adb shell input text "{message}"'
    os.system(command)
    time.sleep(1)

def goback(key_code):
    for i in range(6):
        keyEvent(key_code)

def replace_spaces_with_percent_s(input_string):
    return input_string.replace(' ', '%s')

def markdown_to_text(md):
    html = markdown2.markdown(md)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text().strip()