import asyncio
import edge_tts
import pygame
import os

# Voice Options (You can change this)
# "en-US-AriaNeural" -> Female, very realistic
# "en-US-ChristopherNeural" -> Male, deep and calm
# "en-IN-NeerjaNeural" -> Indian English (Female)
# "en-IN-PrabhatNeural" -> Indian English (Male)
VOICE = "en-US-ChristopherNeural"
OUTPUT_FILE = "speech.mp3"

async def text_to_speech_edge(text):
    # 1. Communicate with Microsoft Edge TTS
    communicate = edge_tts.Communicate(text, VOICE)
    
    # 2. Save audio to a file
    await communicate.save(OUTPUT_FILE)

    # 3. Play the audio using pygame
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()

        # Wait until the audio finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        # Clean up: Delete the file after playing
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)

def speak_realistic(text):
    # Wrapper to run the async function synchronously
    try:
        asyncio.run(text_to_speech_edge(text))
    except Exception as e:
        print(f"Error in TTS: {e}")

# Test it directly if you run this file
if __name__ == "__main__":
    speak_realistic("Hello! I am Vaytron, your realistic AI assistant.")