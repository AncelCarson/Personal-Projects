# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 5/10/2024
### Updated: 30/12/2025
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
import subprocess
from time import time
from dotenv import load_dotenv
from Jeeves_mk3 import loadBot
import Modules.User_Processor as UP
from TextHandler_mk3 import TextHandler

load_dotenv()
REBOOT = os.getenv('REBOOT')
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
      discordThread.start()

   running = True

   activeSessions = []
   activeQueues = {}
   activeHandlers = {}
   activeThreads = {}

   def _flagAction(flag, sessionID):
      """Performs actions on the threads based on Text Handler input
      
      Parameters:
         flag (str): Action to be performed
         sessionID (str): ID of the session that initiated the action
      """
      if flag == "Close Thread":
         activeHandlers[sessionID].iface.mode = "kill"
         del activeQueues[sessionID]
         del activeHandlers[sessionID]
         del activeThreads[sessionID]
         activeSessions.remove(sessionID)
      elif flag == "Check Threads":
         for session in activeSessions:
            if session == sessionID:
               continue
            handler = activeHandlers[session]
            lastTime = (time() - handler.iface.lastActive)/60
            checkIn = handler.iface.checkIn
            lock = handler.iface.timeoutLock
            message = f"The last message for {session} was received {lastTime:.2f} minutes ago.\n"\
                        f"A checkin has{' not' if checkIn else ''} occured.\n"\
                        f"The thread is{'' if lock else ' not'} locked."
            activeHandlers[sessionID].handlePrint(message)
      elif flag == "Close Threads":
         for session in activeSessions:
            handler = activeHandlers[session]
            message = "The administrator has issued a close threads command. "\
                      "I will close out this conversation in 5 minutes"
            handler.handlePrint(message)
            handler.iface.checkIn = False
            handler.iface.closing = True
            handler.iface.lastActive = time() - (10 * 60)
      elif "DM" in flag:
         _,user,interface = flag.split(":")
         outQueues[interface].put(([f"DM!:!{user}",interface,None,sessionID]))
      elif flag == "Reboot":
         subprocess.call(REBOOT)

   def _processInput(input_queue: queue) -> None:
      ctx = list(input_queue.get())
      # ctx = sourceId, Message, Source, Location
      userID = UP.getID(ctx[0], ctx[2])
      print(f"{userID}_{ctx[2]}_{ctx[3]}")
      if userID is not None:
         ctx[0] = userID
         userName = UP.getName(userID)
      else:
         userName = "new user"
      sessionID = f"{ctx[0]}_{ctx[2]}_{ctx[3]}"

      if sessionID not in activeSessions:
         activeSessions.append(sessionID)
         initMsg = f"New thread Initalizing for {userName}"
         output_queue.put((initMsg, "cmd", "term"))
         activeQueues[sessionID] = [queue.Queue(),output_queue]
         activeHandlers[sessionID] = TextHandler(activeQueues[sessionID], ctx[0],
                                                UP.getTitle(userID), ctx[2], ctx[3])
         activeThreads[sessionID] = threading.Thread(target=activeHandlers[sessionID], daemon=True)
         activeThreads[sessionID].start()

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
      activeHandlers[sessionID].user.interface = ctx[2]
      activeHandlers[sessionID].user.location = ctx[3]

      activeQueues[sessionID][0].put(ctx[1])

   def _processOutput(output_queue: queue) -> None:
      ctx = list(output_queue.get())
      # ctx = Message, Destination, Location, UserID
      if "!:!" in ctx[0]:
         sessionID = f"{ctx[3]}_{ctx[1]}_{ctx[2]}"
         flag,msg = ctx[0].split("!:!")
         _flagAction(flag,sessionID)
         if msg == "":
            return
         ctx[0] = msg
      outQueues[ctx[1]].put((ctx))

   while running:
      # Check for messages in the input queue
      if not input_queue.empty():
         _processInput(input_queue)

      # Additional logic or cleanup can go here
      if not output_queue.empty():
         _processOutput(output_queue)

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
