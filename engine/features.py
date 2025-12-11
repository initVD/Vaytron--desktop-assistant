import os
import re
import eel
import pyautogui
import screen_brightness_control as sbc
from AppOpener import open as appopen
import pywhatkit
import google.generativeai as genai
import psutil
import requests
import hashlib
from bs4 import BeautifulSoup
from docx import Document
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from engine.config import ASSISTANT_NAME, GEMINI_API_KEY

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')
chat_session = model.start_chat(history=[
    {"role": "user", "parts": ["You are Vaytron. Answer short and concisely."]},
    {"role": "model", "parts": ["Okay."]}
])

# --- HELPER: Safe Speak Function ---
def speak(text):
    # This imports the function only when needed to prevent circular error
    from engine.command import speak as sp
    sp(text)

# --- FEATURES ---

def openCommand(query):
    query = query.lower().replace("open", "").replace("launch", "").strip()
    if isinstance(ASSISTANT_NAME, list):
        for name in ASSISTANT_NAME: query = query.replace(name.lower(), "")
    else: query = query.replace(ASSISTANT_NAME.lower(), "")
    
    if query != "":
        speak("Opening " + query)
        try: appopen(query, match_closest=True, throw_error=True)
        except: os.system('start ' + query)

def system_stats():
    cpu = psutil.cpu_percent()
    battery = psutil.sensors_battery()
    msg = f"CPU is at {cpu} percent."
    if battery: msg += f" Battery is at {battery.percent} percent."
    speak(msg)

def check_password_safety(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    try:
        res = requests.get('https://api.pwnedpasswords.com/range/' + sha1[:5], timeout=5)
        if sha1[5:] in res.text: speak("Alert! Password found in data breaches.")
        else: speak("Password seems safe.")
    except: speak("Could not check password database.")

def research_topic(topic):
    speak(f"Researching {topic}...")
    try:
        res = requests.get(f"https://www.google.com/search?q={topic}", headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        results = [r.get_text() for r in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')[:5]]
        
        doc = Document()
        doc.add_heading(topic, 0)
        for line in results: doc.add_paragraph(line)
        filename = f"{topic.replace(' ', '_')}.docx"
        doc.save(filename)
        speak("Report saved.")
        os.system(f"start {filename}")
    except: speak("Research failed.")

def open_social_media(platform):
    speak(f"Opening {platform}...")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(f"https://{platform}.com")
    except: speak("Could not open browser.")

# --- CHAT LOGIC ---
def chatWithBot(query):
    eel.DisplayMessage("Thinking...")
    
    # 1. Try Gemini (Online)
    try:
        response = chat_session.send_message(query)
        speak(response.text.replace("*", ""))
    except Exception as e:
        print(f"Gemini Error: {e}. Switching to Offline...")
        
        # 2. Try Llama (Offline)
        try:
            url = "http://localhost:11434/api/generate"
            data = {"model": "llama3", "prompt": query, "stream": False}
            res = requests.post(url, json=data, timeout=5)
            speak(res.json()['response'])
        except:
            speak("I am currently unavailable.")