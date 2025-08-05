# pylint: disable=invalid-name,non-ascii-name,broad-exception-caught,unused-import
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 5/10/2024
### Updated: 5/8/2025
### Windows 11
### Python command line, Notepad, IDLE
### TextHandler_mk2.py

"""Text processing for Jeeves mk3.

This program takes in the text from Jeeves and routes it to the correct
location for processing. Once a response is recieved, it processes it and
prints it to the correct location.

Classes:
    userData: Imformation about the user who started the thread
    threadData: Instance information about the thread
    TextHandler: Class made to handle incoming and outgoing text

Functions:
    main: Driver of the program
    day_greeting: Sends a greeting to the user based on the time of day
    responseTest: Tests the subprocess input and output
"""

# Libraries
import os
import queue
from time import sleep, time
from threading import Thread
from datetime import datetime
from dataclasses import dataclass
from dotenv import load_dotenv

import Modules.User_Processor as UP
from Modules.Roller import roller
from Modules.MenuMaker import menu
from Modules.MenuMaker import makeMenu
from Modules.User_Processor import User_Processor as UPC

load_dotenv()
BOT_LOG = os.getenv('BOT_LOG')
ENV = os.getenv('ENV')

@dataclass
class userData:
    """User Information for the instance.

    Attributes:
        userID (str/int): Id of the user sending a message
        title (str): Title of the user
        interface (str): What interface the message was recieved from
        location (str): Responses to messages recieved from user
    """
    userID: str
    title: str
    interface: str
    location: str

@dataclass
class threadData:
    """Thread Information for the instance.

    Attributes:
        queues (tuple -> Queue): Input and Output queues
        mode (str): Current mode of the program
        thread (thread): Thread used to process a recieved message
        responseQueue (Queue): Input Queue for subprograms
        lastActive (time): The time of the last mesesage from the user
        checkIn (bool): If the handler should give a check in before closing an instance
    """
    queues: tuple[queue.Queue]
    mode: str
    thread: Thread
    responseQueue: queue.Queue
    lastActive: time
    checkIn: bool

# Object Class
class TextHandler:
    """Text processor.

    Attributes:
        queues (tuple -> Queue): Input and Output queues
        userID (str/int): Id of the user sending a message
        title (str): Title of the user
        interface (str): What interface the message was recieved from
        location (str): Responses to messages recieved from user
        mode (str): Current mode of the program
        thread (thread): Thread used to process a recieved message
        responseQueue (Queue): Input Queue for subprograms
        lastActive (time): The time of the last mesesage from the user
        checkIn (bool): If the handler should give a check in before closing an instance

    Functions:
        run: 
        messageIn: Directs an incoming message to the correct location
        handlePrint: A custom print function that can get passed to as sub program
        handleInput: A custom input function that can get passed to as sub program
        setMode: Sets the mode of the handler from an external source 
    """
    def __init__(self, queues=None, userID=None, title="...you", interface="cmd", location="term"):
        self.user = userData(userID, title, interface, location)
        self.iface = threadData(queues, "idle", None, queue.Queue(), time(), True)

    def __call__(self):
        message = f"Thread for {self.user.userID} has been called"
        self.iface.queues[1].put((message,"cmd","term","admin"))
        self.run()

    def __enter__(self):
        pass

    def __exit__(self, *exc):
        pass

    def run(self) -> None:
        """Starts the text processing thread loop for the queue"""
        while self.iface.mode != "kill":
            if self.iface.mode == "thinking":
                if not self.iface.thread.is_alive():
                    self.iface.mode = "idle"
            try:
                message = self.iface.queues[0].get(timeout=.1)
                self.messageIn(message)
                self.iface.lastActive = time()
                self.iface.checkIn = True
            except queue.Empty:
                pass
            if self.iface.mode == "waiting":
                if self.iface.checkIn:
                    if time() - self.iface.lastActive > (30 * 60): #30 minute Timeout
                        self.handlePrint(f"Pardon me {self.user.title}, "\
                                         "I am still awaiting your response.")
                        self.handlePrint("I will maintain this line of query for "\
                                         "another 15 minutes before closing it out.")
                        self.iface.lastActive = time()
                        self.iface.checkIn = False
                        print(f'A check in for thread {self} has occured')
                else:
                    if time() - self.iface.lastActive > (15 * 60): #15 minute Timeout
                        self.handlePrint('Close Thread!:!I have closed this line of query. '\
                                         'To restart simply enter the initial command again.')
            elif self.iface.mode == "idle":
                if time() - self.iface.lastActive > (15 * 60): #15 minute Timeout
                    self.handlePrint('Close Thread!:!')
        print(f'Thread {self} has been killed')

    def messageIn(self, message: str) -> None:
        """Splits incoming messages and sorts them via keywords.

        Parameters:
            message: User input to start process or respond to existing process
        """
        text=[]

        if self.iface.mode == "thinking":
            text = [f"One monent {self.user.title}. I am processing the last request"]

        elif self.iface.mode == "waiting":
            self.iface.responseQueue.put(message)

        elif self.iface.mode == "idle":

            content = message.split(' ')

            if ENV == "test":
                commandDict = {
                    "Jeeves": Tasks.Jeeves,
                    "Response": Tasks.Response,
                    "admin": Tasks.admin,
                }
            else:
                commandDict = {
                    "Jeeves": Tasks.Jeeves,
                    "DM": Tasks.DM,
                    "Response": Tasks.Response,
                    "roll": Tasks.roll,
                    "admin": Tasks.admin,
                }

            try:
                if content[0] in commandDict:
                    text = commandDict[content[0]](content, self)

            except Exception as e:
                text = [f"Something has gone wrong. Please ask again: {e}"]
                print(e)

        for line in text:
            self.handlePrint(line)

    def handlePrint(self, message: str) -> None:
        """Custom Print Statement to be passed to sub programs.

        Parameters:
            message: Message to be sent to the interface
        """
        self.iface.queues[1].put((message,self.user.interface,self.user.location,self.user.userID))

    def handleInput(self, message: str) -> object:
        """Custom Input Statement to be passed to sub programs.

        Parameters:
            message: Message to be sent to the interface

        Returns:
            response (object): Message recieved from the user
        """
        self.iface.queues[1].put((message,self.user.interface,self.user.location,self.user.userID))
        response = self.iface.responseQueue.get()
        self.iface.mode = "thinking"
        return response

    def setMode(self, mode: str):
        """Sets the mode of the thread from an external source.

        Parameters:
            mode: The mode the thread should be set to
        """
        if mode == "kill" and self.user.userID != None:
            return [f"Close Thread!:!The handler mode will be set to {mode}"]

        self.iface.mode = mode
        return [f"The handler mode has been set to {mode}"]

class Tasks:
    """Class Docstring.

    Functions:
        Jeeves: Checks the bot state and user information
        DM: Initializes a Direct Message Conversdation
        Response: Tests Creation of sub threads
        roll: Initialized the roller module
        admin: Handles admin requests
    """

    @staticmethod
    def Jeeves(_: str, handler: TextHandler) -> str:
        """Returns a greeting to the user.
        
        Parameters:
            _ (str): The message in from the user
            handler (TesxHandler): Instance of the text handler

        Returns:
            _ (str): The massage back out to the user
        """
        greeting = day_greeting()
        return [f"Good {greeting[0]} {handler.user.title}. {greeting[1]}"]

    @staticmethod
    def DM(content: str, handler: TextHandler) -> str:
        """Sends a DM to the user for information.
        
        Parameters:
            content (str): The message in from the user
            handler (TesxHandler): Instance of the text handler

        Returns:
            _ (str): The massage back out to the user
        """
        if len(content) != 1:
            if UP.getPermission(handler.user.userID) == "Admin":
                handler.handlePrint(f'DM User:{content[1]}!:!A DM will now be sent')
                return ""
        handler.iface.mode = "thinking"
        userInstance = UPC(handler.user.interface, handler.handleInput, handler.handlePrint)
        data = handler, day_greeting()[0]
        handler.iface.thread = Thread(target=userInstance.aboutYou, args = data, daemon=True)
        handler.iface.thread.start()
        return ""

    @staticmethod
    def Response(_: str, handler: TextHandler) -> str:
        """Creates a thread and asks some quesitons.
        
        Parameters:
            _ (str): The message in from the user
            handler (TesxHandler): Instance of the text handler

        Returns:
            _ (str): The massage back out to the user
        """
        handler.iface.mode = "thinking"
        io = handler.handleInput, handler.handlePrint
        handler.iface.thread = Thread(target=responseTest, args = io, daemon=True)
        handler.iface.thread.start()
        return ""

    @staticmethod
    def roll(content: str, _: TextHandler) -> str:
        """gets a response from the roller module.

        Parameters:
            content (str): The message in from the user
            _ (TextHandler): Instance of the text handler

        Returns:
            _ (str): The massage back out to the user
        """
        if len(content) == 1:
            content.append("help")
        return [roller(content[1:])]

    @staticmethod
    def admin(content: str, handler: TextHandler) -> str:
        """Processes Admin Commands.

        Parameters:
            content (str): The message in from the user
            handler (TesxHandler): Instance of the text handler

        Returns:
            _ (str): The massage back out to the user
        """

        if ENV != "test" and UP.getPermission(handler.user.userID) != "Admin":
            return [f"I am sorry {handler.user.title}, you do not have the required permissions."]

        if len(content) == 1:
            return ["Additional Admin Command Required"]

        def log():
            with open(BOT_LOG, 'r', encoding="utf-8") as file:
                contents = file.read()
            os.system(f"> {BOT_LOG}")  # Clears the file
            if len(contents) > 2000:
                contents = list(contents[0+i:2000+i] for i in range(0, len(contents), 2000))
            else:
                contents = [contents]
            return contents

        if ENV == "test":
            adminDict = {
                "test": lambda: ["You got the test message"],
                "kill": lambda: handler.setMode("kill"),
                # "reboot":os.system('reboot'),
                # "thread":None
            }
        else:
            adminDict = {
            "log": log,
        }

        if content[1] in adminDict:
            return adminDict[content[1]]()

        return""

# Main Function
def main():
    """Launches the TextHandler class and contains the run loop."""
    queues = [queue.Queue(),queue.Queue()]
    handlerThread = Thread(target=TextHandler(queues = queues), daemon = True)
    inputThread = Thread(target=cmdTerm,args=(queues[0],queues[1]), daemon=True)
    handlerThread.start()
    inputThread.start()
    while True:
        while not queues[1].empty():
            print(queues[1].get()[0])
        sleep(1)

def day_greeting() -> list[str]:
    """Gives a user response message based on the time of day."""
    hour = datetime.now().hour
    if hour < 4:
        timePhrase = "morning"
        greeting = "Up late are we?"
    elif hour < 6:
        timePhrase = "morning"
        greeting = "Up early are we?"
    elif hour < 12:
        timePhrase = "morning"
        greeting = "I am listening."
    elif hour < 16:
        timePhrase = "afternoon"
        greeting = "I am listening."
    elif hour < 23:
        timePhrase = "evening"
        greeting = "I am listening."
    else:
        timePhrase = "evening"
        greeting = "Will this be another long night?"

    return [timePhrase, greeting]

def responseTest(handleIn, handleOut):
    """Tests the Response processing of the text handler.
    
    Parameters:
        handleIn (Input): Custom Input Statement for the Text Handler
        handleOut (Print): Custom Output Statement for the Text Handler
    """
    handleOut("This is a call and response test")
    response1 = handleIn("What is response 1?")
    response2 = handleIn("What is response 2?")
    handleOut("Pause for effect")
    sleep(5)
    response3 = handleIn("Response 3?")
    handleOut(f"Here is what you said\n> {response1}\n> {response2}\n> {response3}")

def cmdTerm(input_queue,_):
    """Terminal Interface"""
    while True:
        input_queue.put(input())

# Self Program Call
if __name__ == '__main__':
    main()
