# pylint: disable=invalid-name,bad-indentation,non-ascii-name,broad-exception-caught,unused-import
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 5/10/2024
### UPdated: 7/10/2024
### Windows 11
### Python command line, Notepad, IDLE
### TextHandler_mk2.py

"""Text processing for Jeeves mk2.

This program takes in the text from Jeeves and routes it to the correct
location for processing. Once a response is recieved, it processes it and
prints it to the correct location. 

Classes:
    TextHandler: Class made to handle incoming and outgoing text

Functions:
   main: Driver of the program
   day_greeting: Sends a greeting to the user based on the time of day
   responseTest: Tests the subprocess input and output
"""

# Libraries
import os
import queue
from time import sleep
from threading import Thread
from datetime import datetime

from Modules.Roller import roller
from Modules.MenuMaker import menu
from Modules.MenuMaker import makeMenu

# Object Class
class TextHandler:
    """Class Docstring.

    Variables:
        queues (List -> Queue): Input and Output queues
        userId (str/int): Id of the user sending a message
        title (str): Title of the user
        interface (str): What interface the message was recieved from
        location (str): Responses to messages recieved from user
        mode (str): Current mode of the program
        _thread (thread): Thread used to process a recieved message
        responseQueue (Queue): Input Queue for subprograms
    
    Functions:
        messageIn: Directs an incoming message to the correct location
        responseIn: Creates a thread for processing a response
        responseProcess: A test for handling sequential responses
    """
    def __init__(self, queues=None, userId=None, title="...you", interface="cmd", location="term"):
        self.queues = queues
        self.userId = userId
        self.title = title
        self.interface = interface
        self.location = location
        self.mode = "idle"
        self._thread = None
        self.responseQueue = queue.Queue()

    def __call__(self):
        message = f"Thread for {self.userId} has been called"
        self.queues[1].put((message,"cmd","term"))
        self.run()

    def __enter__(self):
        pass

    def __exit__(self, *exc):
        pass

    def run(self):
        """Starts the text processing thread loop for the queue"""
        while self.mode != "kill":
            try:
                message = self.queues[0].get(timeout=.1)
                self.messageIn(message)
            except queue.Empty:
                continue

    def messageIn(self, message: str):
        """Splits incoming messages and sorts them via keywords.
        
        Parameters:
            self: TextHandler Instance
            message: User input to start process or respond to existing process
        """
        text=[]

        if self.mode == "thinking":
            text = [f"One monent {self.title}. I am processing the last request"]

        if self.mode == "waiting":
            self.responseQueue.put(message)

        if self.mode == "idle":
            greeting = day_greeting()

            content = message.split(' ')
            try:
                if content[0] == "Jeeves":
                    text = [f"Good {greeting[0]} {self.title}. {greeting[1]}"]

                if content[0] == "DM":
                    self.mode = "userSetTest"
                    text = [f'Good {greeting[0]} {content[1]}. I am here to assist you',
                            "Would you please tell me your First and Last Name?",
                            "Are you Male (M) or Female (F)?",
                            "Please answer with a single Character"]

                if content[0] == "Response":
                    self.mode = "thinking"
                    io = self.handleInput, self.handlePrint
                    self._thread = Thread(target=responseTest, args = io, daemon=True)
                    self._thread.start()
                    self.mode = "idle"

                if content[0] == "roll":
                    if len(content) == 1:
                        content.append("help")
                    text = [roller(content[1:])]

            except Exception as e:
                text = [f"Something has gone wrong. Please ask again: {e}"]
                print(e)

        for line in text:
            self.queues[1].put((line,self.interface,self.location))

    def handlePrint(self, message: str):
        """Custom Print Statement to be passed to sub programs.
        
        Parameters:
            self: TextHandler Instance
            message: Message to be sent to the interface
        """
        self.queues[1].put((message,self.interface,self.location))

    def handleInput(self, message: str):
        """Custom Input Statement to be passed to sub programs.
        
        Parameters:
            self: TextHandler Instance
            message: Message to be sent to the interface

        Returns:
            response (str): Message recieved from the user
        """
        self.mode = "waiting"
        self.queues[1].put((message,self.interface,self.location))
        response = self.responseQueue.get()
        self.mode = "thinking"
        return response

# Main Function
def main():
    """Launches the TextHandler class and contains the run loop."""
    queues = [queue.Queue(),queue.Queue()]
    thread = Thread(target=TextHandler(queues = queues), daemon = True)
    thread.start()
    while True:
        if not queues[1].empty():
            print(queues[1].get()[0])
        queues[0].put(input())
        sleep(1)

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

def responseTest(handleIn, handleOut):
    """Tests the Response processing of the text handler.
    
    Parameters:
        handleIn (Input): Custom Input Statement for the Text Handler
        handleOut (Print): Custom Output Statement for the Text Handler
    """
    handleOut("This is a call and response test")
    handleIn("What is response 1?")
    handleIn("What is response 2?")
    handleOut("Pause for effect")
    handleIn("Response 3?")

# Self Program Call
if __name__ == '__main__':
    main()
