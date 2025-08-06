# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 5/10/2024
### Updated: 5/8/2025
### Windows 11
### Python command line, VSCode
### StartFile.py

"""Data sorter for the Jeeves Project.

This program will initializeall of the interfaces that Jeeves has access to. It
will then sort incoming data to TextHandlers for processing user requests and 
responses. It does this by managing various queues and threads between all modules.

Functions:
   main: Driver of the program
"""

# Libraries
import os
import queue
import threading
from time import time
from dotenv import load_dotenv
from Jeeves_mk3 import loadBot
import Modules.User_Processor as UP
from TextHandler_mk3 import TextHandler

load_dotenv()
ENV = os.getenv('ENV')

# Main Function
def main():
   """Driver of the Program"""
   # Create the shared queues
   input_queue = queue.Queue()
   output_queue = queue.Queue()
   outQueues = {
      "cmd": queue.Queue(),
      "Discord": queue.Queue(),
   }

   # Initializing interface threads
   discordThread = threading.Thread(target=loadBot,
                   args=(input_queue, outQueues["Discord"]), daemon=True)
   commandThread = threading.Thread(target=cmdTerm,
                   args=(input_queue, outQueues["cmd"]), daemon=True)

   # Starting interface Threads
   if ENV != "test":
      discordThread.start()
   else:
      commandThread.start()

   running = True

   activeUsers = []
   activeQueues = {}
   activeHandlers = {}
   activeThreads = {}

   def flagAction(flag, userID):
      """Performs actions on the threads based on Text Handler input
      
      Parameters:
         flag (str): Action to be performed
         userID (str): ID of the user who initiated the action
      """
      if flag == "Close Thread":
         activeHandlers[userID].iface.mode = "kill"
         del activeQueues[userID]
         del activeHandlers[userID]
         del activeThreads[userID]
         activeUsers.remove(userID)
      elif flag == "Check Threads":
         for user in activeUsers:
            if user == userID:
               continue
            handler = activeHandlers[user]
            lastTime = (time() - handler.iface.lastActive)/60
            checkIn = handler.iface.checkIn
            message = f"The last message for {user} was received {lastTime:.2f} minutes ago.\n"\
                        f"A checkin has{"" if checkIn else " not"} occured"
            activeHandlers[userID].handlePrint(message)
      elif flag == "Close Threads":
         for user in activeUsers:
            handler = activeHandlers[user]
            message = "The administrator has issued a close threads command. "\
                      "I will close out this conversation in 5 minutes"
            handler.handlePrint(message)
            handler.iface.checkIn = True
            handler.iface.closing = True
            handler.iface.lastActive = time() - (10 * 60)
            # flagAction("Close Thread", user)

   while running:
      # Check for messages in the input queue
      if not input_queue.empty():
         ctx = list(input_queue.get())
         # ctx = sourceId, Message, Source, Location
         userID = UP.getID(ctx[0], ctx[2])
         if userID is not None:
            ctx[0] = userID
            userName = UP.getName(userID)
         else:
            userName = "new user"

         if ctx[0] not in activeUsers:
            activeUsers.append(ctx[0])
            initMsg = f"New thread Initalizing for {userName}"
            output_queue.put((initMsg, "cmd", "term"))
            activeQueues[ctx[0]] = [queue.Queue(),output_queue]
            activeHandlers[ctx[0]] = TextHandler(activeQueues[ctx[0]], ctx[0],
                                                 "Sir", ctx[2], ctx[3])
            activeThreads[ctx[0]] = threading.Thread(target=activeHandlers[ctx[0]], daemon=True)
            activeThreads[ctx[0]].start()

         # Process the message, add flags, and direct it to the appropriate program
         print(f"{ctx[2]} passed message for {userName}: {ctx[1]}")
         if "some condition" in ctx[1]:
            # Modify the message if necessary and forward it to a secondary program
            input_queue.put(("flagged_message", ctx[1]))
         else:
            # Handle or route the message as needed
            pass

         # TODO: Remove this when multi-channel thread logic is implemented.
         # Makes the bot respond to the thread the question was asked in.
         activeHandlers[ctx[0]].user.interface = ctx[2]
         activeHandlers[ctx[0]].user.location = ctx[3]

         activeQueues[ctx[0]][0].put(ctx[1])

      # Additional logic or cleanup can go here
      if not output_queue.empty():
         ctx = list(output_queue.get())
         if "!:!" in ctx[0]:
            flag,msg = ctx[0].split("!:!")
            flagAction(flag,ctx[3])
            if msg == "":
               continue
            ctx[0] = msg
         # ctx = Message, Destination, Location, UserID
         outQueues[ctx[1]].put((ctx))

      if not outQueues["cmd"].empty():
         ctx = outQueues["cmd"].get()
         # ctx = Message, Destination, Location, UserID
         print(ctx[0])

def cmdTerm(input_queue,_):
   """Terminal Interface"""
   while True:
      input_queue.put(("admin",input(),"cmd","term"))

# Self Program Call
if __name__ == '__main__':
   main()
