import asyncio
import edge_tts
import pygame
import os

VOICE = "en-US-ChristopherNeural"
OUTPUT_FILE = "speech.mp3"

async def text_to_speech_edge(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        # CRITICAL FIX: Stop and Quit to release file lock so we can delete it
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)

def speak_realistic(text):
    try:
        asyncio.run(text_to_speech_edge(text))
    except Exception as e:
        print(f"Error in TTS: {e}")