# pylint: disable=invalid-name,bad-indentation,non-ascii-name,unused-import,global-statement
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 5/10/2024
### UPdated: 5/10/2024
### Windows 11
### Python command line, Notepad, IDLE
### Jeeves_mk3.py

"""A discord bot that functions as an interface to various other programs.

Jeeves is the discord interface to a series of other programs to assist in various
tasks. The program will manage the discord specific interactions as well as pass
requests onto the TextHandler

Variables:
    TOKEN (str): Discord bot connection Id
    GUILD (int): Server Id for connection
    intents (object): Initilizing details for discord bot
    client (?): Client Connection Credentialls
    activeUsers (list -> int):
    activeThreads (list -> thread):

Functions:
   on_ready: Actions to perform on successful startup
   on_reaction_add: Actions to perform when a reaction is added
   on_member_join: Actions to perform when a new member joins
   on_message: Actions to perform when a message is recieved
   getAnswers: sends messages from user to the TextHandler
   response_get: Gets responses from user to messages sent by the bot
   sender: Sends messages to Discord
"""

# Libraries
import os
import asyncio
from time import sleep
from datetime import datetime

import discord
from dotenv import load_dotenv

#creating a new discord client for us to use. cool_bot be the client
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = int(os.getenv('GUILD_TOKEN'))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client=discord.Client(intents=intents)
#methods waiting for the event

activeUsers = []
activeThreads = []

bot_in = None
bot_out = None

#================   On Bot Boot      ================
@client.event
async def on_ready():
    """Prints to terminal that the bot is connected properly."""
    guild = client.get_guild(GUILD)
    print(
        f'{client.user} is connected to:',
        f'{guild.name} - id: {guild.id}',
        sep='\n')
    await send_bot_out()

#================   On Reaction Add     ================
@client.event
async def on_reaction_add(reaction, user):
    """Sets user role based on reaction selection."""
    if user == client.user:
        return
    message = reaction.message

    if message.guild is None: #this is a dm message
        guild = client.get_guild(GUILD)
        Madam = guild.get_role(1061842851220160664)
        Monsieur = guild.get_role(1061842845981491221)
        member = guild.get_member(user.id)
        if str(reaction) == '\U0001F1EB':
            await member.add_roles(Madam, reason="Preference Set")
        if str(reaction) == '\U0001F1F2':
            await member.add_roles(Monsieur, reason="Preference Set")
        await member.dm_channel.send("Thank you for making your selection")
        await member.dm_channel.send("Your role has been updated accordingly")

#================   On Member Join      ================
@client.event
async def on_member_join(member):
    """Requests title assignment when a new member joins."""
    await member.create_dm()
    await bot_in.put((member.id,f"DM {member.name}","Discord",member.dm_channel))
    await asyncio.sleep(5)
    message = "Please react below whether you are Male 'M' or Female 'F'"
    msg = await member.dm_channel.send(message)
    await msg.add_reaction('\U0001F1F2') #M
    await msg.add_reaction('\U0001F1EB') #F

#================   On Message      ================
@client.event
async def on_message(message):
    """Recieves in message from Discord and passes it to the TextHandler."""
    UserId = message.author.id

    # Check that Jeeves does nto respond to his own message.
    if UserId == client.user.id:
        return

    if message.content.startswith('Bot Check'):
        await message.channel.send(f'Hello {message.author.mention} Bot is Running')
        await message.channel.send('Jeeves is awaiting your command.')
        return

    if not message.content.startswith('!'):
        return

    if UserId not in activeUsers:
        for role in message.author.roles:
            if role.id == 1061842845981491221:
                title = "Sir"
            elif role.id == 1061842851220160664:
                title = "Madam"
            else: title = "...you"

        activeUsers.append(UserId)
        # activeThreads.append(TextHandler(UserId,title,"Discord"))

    bot_in.put((UserId,message.content[1:],"Discord",message.channel))
    # userIndex = activeUsers.index(UserId)
    # thread = activeThreads[userIndex]

    # text = thread.messageIn(message.content)
    # # print(text)
    # # async def textProcessor(text):
    # answers = await getAnswers(text, message)

    # if len(answers) > 0:
    #     thread.channel = message.channel
    #     thread.responseIn(answers)

#================   Non Event Functions      ================

# async def getAnswers(text, message):
#     """Recieves answers from the TextHandler to be sent to the user."""
#     answers = []
#     if len(text) == 0:
#         return answers
#     for line in text:
#         if line[1] == 0:
#             await sender(message, line[0])
#         elif line[1] == 1:
#             try:
#                 answers.append(await response_get(message, line[0], 10))
#             except asyncio.TimeoutError:
#                 missedText = "I am sorry, I did not catch all of that " \
#                             "can you please start again from the beginning?"
#                 await sender(message, missedText)
#                 return []
#     return answers

# async def response_get(ctx, message: str,timeout: float):
#     """Handles interactions that require responses to messages sent by the bot."""
#     def check(m):
#         return m.author == ctx.author and m.channel == ctx.channel

#     await sender(ctx, message)
#     response = await client.wait_for("message", check=check, timeout=timeout)
#     print(response.content)
#     return response.content

# async def sender(ctx, message: str):
#     """Sends Messages to Discord"""
#     await ctx.channel.send(message)

async def send_bot_out():
    """Function Docstring"""
    while True:
        if not bot_out.empty():
            content, _, channel = bot_out.get()
            await channel.send(content)
        await asyncio.sleep(1)

def loadBot(input_queue: str, output_queue: str):
    """Function Docstring"""
    asyncio.run(runBot(input_queue, output_queue))
    client.run(TOKEN)

async def runBot(input_queue: str, output_queue: str):
    """Function Docstring"""
    global bot_in, bot_out
    bot_in = input_queue
    bot_out = output_queue

#finnaly we have to run our bot. previous stuffs are defining the functions of the bot
if __name__ == '__main__':
    import queue
    runBot(queue.Queue(), queue.Queue())
    client.run(TOKEN)
