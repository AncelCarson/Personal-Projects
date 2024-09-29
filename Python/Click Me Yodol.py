# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### 2/24/2020
### Windows 10
### Python command line, Notepad, IDLE

"""A simple script to mess with a dormmate if he was on my computer."""

# Libraries
import os
import ctypes
import time
from pynput.mouse import Listener

# Main Function
def main():
    """Main Driver tha loads other functions."""
    AudioSwitch()
    Dipper()
    Lock()

#Audio Correction
def AudioSwitch():
    """Switches the audio device to the speaker."""
    os.startfile(r'C:\Users\Ancel Carson\Documents\Coding\Python\Anti Yodol Box\AudioSelect.vbs')
    time.sleep(.5)

#Visualizer and Video
def Dipper():
    """Starts the aidion vizualizer and loads video."""
    os.startfile(r'C:\Users\Ancel Carson\Razer\Audio_Visualizer\KeyboardVisualizerVC 3.04.exe')
    time.sleep(.5)
    os.startfile(r'C:\Users\Ancel Carson\Documents\Coding\Python\Anti Yodol Box'
                r'\You_shouldnt_have_done_that.mp4')
    time.sleep(9)

#Locks Computer
def Lock():
    """Locks the machine."""
    ctypes.windll.user32.LockWorkStation()

# Self Program Call
if __name__ == '__main__':
    main()
