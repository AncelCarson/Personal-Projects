### Ancel Carson
### 2/24/2020
### Windows 10
### Python command line, Notepad, IDLE

# Libraries
import os
import sys
import ctypes
import time
from pynput.mouse import Listener

run = False

# Main Function
def on_click(x, y, button, pressed):
    global run
    if(run == True):
        AudioSwitch()
        Dipper()
        Lock()
        sys.exit()
    time.sleep(10)
    run = True

#Audio Correction
def AudioSwitch():
    os.startfile(r'C:\Users\Ancel Carson\Documents\Coding\Python\Anti Yodol Box\AudioSelect.vbs')
    time.sleep(.5)

#Visualizer and Video
def Dipper():
    os.startfile(r'C:\Users\Ancel Carson\Razer\Audio_Visualizer\KeyboardVisualizerVC 3.04.exe')
    time.sleep(.5)
    os.startfile(r'C:\Users\Ancel Carson\Documents\Coding\Python\Anti Yodol Box\You_shouldnt_have_done_that.mp4')
    time.sleep(9)

#Locks Computer
def Lock():
    ctypes.windll.user32.LockWorkStation()



with Listener(on_click=on_click) as listener:
    listener.join()
