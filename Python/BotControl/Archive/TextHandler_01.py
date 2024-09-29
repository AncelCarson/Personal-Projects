# pylint: disable=all
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 8/1/2020
### UPdated: 25/1/2023
### Windows 11
### Python command line, Notepad, IDLE
### TextHandler.py

# Libraries
import os
from time import sleep
from MenuMaker import menu
from datetime import datetime
from MenuMaker import makeMenu

# Object Class
class TextHandler:
    def __init__(self, sender=print,response=input):
        self.sender = sender
        self.response = response

    def hello(self):
        self.sender("Hello")

    def world(self):
        self.sender("World")

    async def messageIn(self, message):
        for role in message.author.roles:
            if role.id == 1061842845981491221: title = "Sir"
            elif role.id == 1061842851220160664: title = "Madam"
            else: title = "...you"

        greeting = day_greeting()

        content = message.content.split(' ')
        if content[0] == "/Jeeves":
            await self.sender(message, "Good {1} {0}. {2}".format(title, greeting[0], greeting[1]))

        if content[0] == "/DM":
            member = message.author
            await member.create_dm()
            await member.dm_channel.send(f'Good {greeting[0]} {member.name}. I am here to assist you')
            msg = await member.dm_channel.send("Please react below weather you are Male 'M' or Female 'F'")
            await msg.add_reaction('\U0001F1F2') #M
            await msg.add_reaction('\U0001F1EB') #F

# Main Function
async def main():
    textHandler = TextHandler()
    while True:
        await textHandler.messageIn(input())

def day_greeting():
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

# Self Program Call
if __name__ == '__main__':
    main()
    # async with TextHandler() as textHandler:
    #     await textHandler.messageIn(input())


    # textHandler = TextHandler()
    # while True:
    #     textHandler.messageIn(input())