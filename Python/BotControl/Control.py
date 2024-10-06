# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 5/10/2024
### Updated: 5/10/2024
### Windows 11
### Python command line, VSCode
### StartFile.py

"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Classes:
    Start:

Functions:
   main: Driver of the program
"""

# Libraries
import threading
import queue
from Jeeves_mk3 import loadBot
from TextHandler_mk3 import TextHandler

# from Roller import roller

# Main Function
def main():
   """Function Docstring."""
   # Create the shared queues
   input_queue = queue.Queue()
   output_queue = queue.Queue()
   outQueues = {
      "cmd": queue.Queue(),
      "Discord": queue.Queue(),
   }

   # Initializing interface threads
   discordThread = threading.Thread(target=loadBot, args=(input_queue, outQueues["Discord"]), daemon=True)

   # Starting interfaace Threads
   discordThread.start()

   running = True

   activeUsers = []
   activeHandlers = {"admin": TextHandler(output_queue, "Admin", "Sir", "cmd", "term")}
   activeThreads = {"admin": threading.Thread(target=activeHandlers["admin"], daemon=True)}

   while running:
      # Check for messages in the input queue
      if not input_queue.empty():
         ctx = input_queue.get()
         # ctx = userId, Message, Source, Location

         if ctx[0] not in activeUsers:
            activeUsers.append(ctx[0])
            initMsg = f"New thread Initalizing for {ctx[0]}"
            output_queue.put((initMsg, "cmd", "term"))
            activeHandlers[ctx[0]] = TextHandler(output_queue, ctx[0], "Sir", ctx[2], ctx[3])
            activeThreads[ctx[0]] = threading.Thread(target=activeHandlers[ctx[0]], daemon=True)
            activeThreads[ctx[0]].start()

         # Process the message, add flags, and direct it to the appropriate program
         print(f"{ctx[2]} passed message for XX: {ctx[1]}")
         if "some condition" in ctx[1]:
            # Modify the message if necessary and forward it to a secondary program
            input_queue.put(("flagged_message", ctx[1]))
         else:
            # Handle or route the message as needed
            pass

         activeHandlers[ctx[0]].messageIn(ctx[1])

      # Additional logic or cleanup can go here
      if not output_queue.empty():
         ctx = output_queue.get()
         # ctx = Message, Destination, Location
         outQueues[ctx[1]].put((ctx))

      if not outQueues["cmd"].empty():
         ctx = outQueues["cmd"].get()
         # ctx = Message, Destination, Location
         print(ctx[0])

# Self Program Call
if __name__ == '__main__':
   main()
