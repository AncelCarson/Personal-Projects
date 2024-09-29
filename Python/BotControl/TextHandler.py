# pylint: disable=invalid-name,bad-indentation,non-ascii-name,broad-exception-caught,unused-import
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 8/1/2020
### UPdated: 8/1/2023
### Windows 11
### Python command line, Notepad, IDLE
### TextHandler.py

"""Text processing for Jeeves mk2.

This program takes in the text from Jeeves and routes it to the correct
location for processing. Once a response is recieved, it processes it and
prints it to the correct location. 

Classes:
    TextHandler: Class made to handle incoming and outgoing text

Functions:
   main: Driver of the program
   day_greeting: Sends a greeting to the user based on the time of day
   sender: Prints any messages to discord or the command line
"""

# Libraries
import os
from time import sleep
from threading import Thread
from datetime import datetime

from Roller import roller
from MenuMaker import menu
from MenuMaker import makeMenu

# Object Class
class TextHandler:
    """Class Docstring.

    Variables:
        userId (str/int): Id of the user sending a message
        title (str): Title of the user
        interface (str): What interface the message was recieved from
        answers (list -> str): Responses to messages recieved from user
        mode (str): Current mode of the program
        channel (int): Discord channel a message was recieved from
        _thread (thread): Thread used to process a recieved message
    
    Functions:
        messageIn: Directs an incoming message to the correct location
        responseIn: Creates a thread for processing a response
        responseProcess: A test for handling sequential responses
    """
    def __init__(self, userId=None, title="...you", interface="cmd"):
        self.userId = userId
        self.title = title
        self.interface = interface
        self.answers = []
        self.mode = "waiting"
        self.channel = None
        self._thread = None

    def __enter__(self):
        pass

    def __exit__(self, *exc):
        pass

    def messageIn(self, message):
        """Splits incoming messages and sorts them via keywords."""
        text=[]

        if self.mode != "waiting":
            if self.mode == "thinking":
                text = [[f"One monent {self.title}. I am processing the last request",0]]
                return text
            return text

        greeting = day_greeting()

        content = message.split(' ')
        try:
            if content[0] == "/Jeeves":
                text = [[f"Good {self.title} {greeting[0]}. {greeting[1]}",0]]

            if content[0] == "/DM":
                self.mode = "userSetTest"
                text = [[f'Good {greeting[0]} {content[1]}. I am here to assist you',0],
                        ["Would you please tell me your First and Last Name?",1],
                        ["Are you Male (M) or Female (F)?",0],
                        ["Please answer with a single Character",1]]

            if content[0] == "/Response":
                self.mode = "responseTest"
                text = [['This is a call and response test',0],
                        ["What is response 1?",1],
                        ["Response 2?",1],
                        ["Pause for effect",0],
                        ["Response 3?",1]]

            if content[0] == "/roll":
                text = [[roller(content[1:]),0]]
                # for line in result:
                #     text.append([str(line),0])


        except Exception as e:
            text = [[f"Something has gone wrong. Please ask again: {e}",0]]

        return text

    def responseIn(self, answers):
        """Creates a thread form processing answers."""
        self.answers = answers
        self._thread = Thread(target=self.responseProcess, daemon=True)
        self._thread.start()
        return "¯\\(°_o)/¯"

    def responseProcess(self):
        """Test for response timing."""
        process = self.mode
        self.mode = "thinking"

        if process == "responseTest":
            print(self.answers)
            for i in range(10):
                print(i)
                sleep(1)
        self.mode = "waiting"

        if process == "userSetTest":
            print(self.answers)
            for i in range(10):
                print(i)
                sleep(1)

        sender(self, "Task Complete")
        self.mode = "waiting"
        return self

# Main Function
def main():
    """Launches the TextHandler class and contains the run loop."""
    textHandler = TextHandler()
    while True:
        answers = []
        text = textHandler.messageIn(input())
        for line in text:
            if line[1] == 0:
                print(line[0])
            elif line[1] == 1:
                answers.append(input(line[0]))
        if len(answers) > 0:
            endMsg = textHandler.responseIn(answers)
            print(endMsg)

def day_greeting():
    """Gives a user response message based on the time of day."""
    hour = datetime.now().hour
    if hour < 4:
        time = "morning"
        greeting = "Up late are we?"
    elif hour < 6:
        time = "morning"
        greeting = "Up early are we?"
    elif hour < 12:
        time = "morning"
        greeting = "I am listening."
    elif hour < 16:
        time = "afternoon"
        greeting = "I am listening."
    elif hour < 23:
        time = "evening"
        greeting = "I am listening."
    else:
        time = "evening"
        greeting = "Will this be another long night?"

    return [time, greeting]

def sender(self, message):
    """Sends generated responses to the correct interface."""
    if self.interface == "cmd":
        print(message)
    if self.interface == "Discord":
        self.channel.send(message)

# Self Program Call
if __name__ == '__main__':
    main()
