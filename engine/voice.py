import asyncio
import edge_tts
import pygame
import os
import pyttsx3 
from langdetect import detect

# 1. Setup Offline Engine First (Reliable Backup)
def speak_offline(text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        # Try to find a female voice, otherwise use default
        engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Offline TTS Error: {e}")

# 2. Setup Online Engine (Realistic)
async def text_to_speech_edge(text):
    OUTPUT_FILE = "speech.mp3"
    voice = "en-US-ChristopherNeural" # Default

    # Auto-detect language
    try:
        lang = detect(text)
        if lang == 'hi': voice = "hi-IN-SwaraNeural"
        elif lang == 'gu': voice = "gu-IN-DhwaniNeural"
    except:
        pass

    try:
        # Create audio file
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(OUTPUT_FILE)

        # Play audio file
        pygame.mixer.init()
        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()

        # Wait until audio is done
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
    except Exception as e:
        # CRITICAL: If anything goes wrong, use Offline Voice
        print(f"Online Voice Failed: {e}")
        speak_offline(text)

    finally:
        # Clean up file
        if os.path.exists(OUTPUT_FILE):
            try:
                os.remove(OUTPUT_FILE)
            except:
                pass

def speak_realistic(text):
    try:
        asyncio.run(text_to_speech_edge(text))
    except Exception as e:
        speak_offline(text)