# pylint: disable=invalid-name,bad-indentation,non-ascii-name,broad-exception-caught,unused-import
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 5/10/2024
### Updated: 22/2/2024
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
from dotenv import load_dotenv

from Modules.Roller import roller
from Modules.MenuMaker import menu
from Modules.MenuMaker import makeMenu

load_dotenv()
BOT_LOG = os.getenv('BOT_LOG')
ENV = os.getenv('ENV')

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
        self.thread = None
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
            if self.mode == "thinking":
                if not self.thread.is_alive():
                    self.mode = "idle"
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

        elif self.mode == "waiting":
            self.responseQueue.put(message)

        elif self.mode == "idle":

            content = message.split(' ')

            commandDict = {
                "Jeeves": Tasks.Jeeves,
                "DM": Tasks.DM,
                "Response": Tasks.Response,
                "roll": Tasks.roll,
                "admin": Tasks.admin,
            }

            if ENV == "test":
                commandDict = {
                    "admin": Tasks.admin,
                }

            try:
                if content[0] in commandDict:
                    text = commandDict[content[0]](content, self)

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

class Tasks:
    """Class Docstring.

    Functions:
        Jeeves: Checks the bot state and user information
        DM: Initializes a Direct Message Conversdation
        Response: Tests Creation of sub threads
        roll: Initialized the roller module
    """

    @staticmethod
    def Jeeves(_, handler):
        """Returns a greeting to the user"""
        greeting = day_greeting()
        return [f"Good {greeting[0]} {handler.title}. {greeting[1]}"]

    @staticmethod
    def DM(content, handler):
        """Sends a DM to the user for information"""
        greeting = day_greeting()
        if len(content) == 1:
            content.append(handler.userId)
        handler.mode = "userSetTest"
        return [f'Good {greeting[0]} {content[1]}. I am here to assist you',
                "Would you please tell me your First and Last Name?",
                "Are you Male (M) or Female (F)?",
                "Please answer with a single Character"]

    @staticmethod
    def Response(_, handler):
        """Creates a thread and asks some quesitons"""
        handler.mode = "thinking"
        io = handler.handleInput, handler.handlePrint
        handler.thread = Thread(target=responseTest, args = io, daemon=True)
        handler.thread.start()
        return ""

    @staticmethod
    def roll(content, _):
        """gets a response from the roller module"""
        if len(content) == 1:
            content.append("help")
        return [roller(content[1:])]

    @staticmethod
    def admin(content, handler):
        """Processes Admin Commands"""

        if len(content) == 1:
            return ["Additional Admin Command Required"]

        def log():
            with open(BOT_LOG, 'r', encoding="utf-8") as file:
                contents = file.read()
            os.system(f"> {BOT_LOG}")  # Clears the file
            return [contents]

        adminDict = {
            "log": log,
        }

        if ENV == "test":
            adminDict = {
                "test": lambda: ["You got the test message"]
                # "reboot":os.system('reboot'),
                # "thread":None
            }

        if content[1] in adminDict:
            return adminDict[content[1]]()

        return""

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
    sleep(5)
    handleIn("Response 3?")

# Self Program Call
if __name__ == '__main__':
    main()
