import os
import eel
from engine.command import *

def start():
    eel.init("www")
    # Launch Edge in App Mode
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    # Start Eel on port 8000
    eel.start('index.html', mode=None, host='localhost', port=8000, block=True)

if __name__ == "__main__":
    start()