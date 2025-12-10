import asyncio
import edge_tts
import pygame
import os
from langdetect import detect

# Default English Voice
DEFAULT_VOICE = "en-US-ChristopherNeural"

# Language Map (Auto-switch voices)
VOICE_MAP = {
    'gu': "gu-IN-DhwaniNeural",   # Gujarati
    'hi': "hi-IN-SwaraNeural",    # Hindi
    'mr': "mr-IN-AarohiNeural",   # Marathi
    'ta': "ta-IN-PallaviNeural",  # Tamil
    'te': "te-IN-ShrutiNeural",
    'kn': "kn-IN-SwaraNeural",    # Telugu
}

async def text_to_speech_edge(text):
    # 1. Determine which voice to use
    voice = DEFAULT_VOICE
    try:
        # Detect language code (e.g., 'en', 'gu', 'hi')
        lang_code = detect(text)
        if lang_code in VOICE_MAP:
            voice = VOICE_MAP[lang_code]
            print(f"Detected {lang_code}: Switching voice to {voice}")
    except Exception as e:
        print(f"Language detection failed, using default: {e}")

    # 2. Generate Audio
    communicate = edge_tts.Communicate(text, voice)
    
    # Define output file
    output_file = "speech.mp3"
    
    # Remove old file if it exists to prevent permission errors
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except PermissionError:
            print("File is locked, skipping delete.")
            return

    await communicate.save(output_file)

    # 3. Play Audio
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        # Stop and Quit to release file lock
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
        # Cleanup
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except:
                pass

def speak_realistic(text):
    try:
        asyncio.run(text_to_speech_edge(text))
    except Exception as e:
        print(f"Error in TTS: {e}")