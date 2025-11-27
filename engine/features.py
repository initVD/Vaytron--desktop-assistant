from playsound import playsound
import eel


#playing assistannt sound function
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\bootup.mp3"
    playsound(music_dir)
    