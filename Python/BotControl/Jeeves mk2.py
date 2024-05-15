### Ancel Carson
### Created: 8/1/2023
### UPdated: 8/1/2023
### Windows 11
### Python command line, Notepad, IDLE
### Jeeves.py

# Libraries
import os
import discord
import asyncio
from time import sleep
from datetime import datetime
from dotenv import load_dotenv
from TextHandler import TextHandler

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

#================   On Bot Boot      ================
@client.event
async def on_ready():
    guild = client.get_guild(GUILD)
    print(
        f'{client.user} is connected to:',
        f'{guild.name} - id: {guild.id}',
        sep='\n')

#================   On Reaction Add     ================
@client.event
async def on_reaction_add(reaction, user):
    if user == client.user: return
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
    with TextHandler() as textHandler:
        text = await textHandler.messageIn(f"/DM {member.name}")
        await member.create_dm()
        await member.dm_channel.send(text[0][0])
        msg = await member.dm_channel.send("Please react below weather you are Male 'M' or Female 'F'")
        await msg.add_reaction('\U0001F1F2') #M
        await msg.add_reaction('\U0001F1EB') #F

#================   On Message      ================
@client.event
async def on_message(message):
    id = message.author.id

    # Check that Jeeves does nto respond to his own message. 
    if id == client.user.id:
        return

    if message.content.startswith('Bot Check'):
        await message.channel.send('Hello {0.author.mention} Bot is Running'.format(message))
        await message.channel.send('Jeeves is awaiting your command.')
        return

    if id not in activeUsers:
        for role in message.author.roles:
            if role.id == 1061842845981491221: title = "Sir"
            elif role.id == 1061842851220160664: title = "Madam"
            else: title = "...you"

        activeUsers.append(id)
        activeThreads.append(TextHandler(id,title,"Discord"))


    userIndex = activeUsers.index(id)
    thread = activeThreads[userIndex]

    text = thread.messageIn(message.content)
    # print(text)
    # async def textProcessor(text):
    answers = await getAnswers(text, message)

    if len(answers) > 0:
        thread.channel = message.channel
        thread.responseIn(answers)

#================   Non Event Functions      ================

async def getAnswers(text, message):
    answers = []
    if len(text) == 0:
        return answers
    for line in text:
        if line[1] == 0:
            await sender(message, line[0])
        elif line[1] == 1:
            try:
                answers.append(await response_get(message, line[0], 10))
            except asyncio.TimeoutError:
                missedText = "I am sorry, I did not catch all of that can you please start again from the beginning?"
                await sender(message, missedText)
                return []
    return answers

async def response_get(ctx, message: str,timeout: float):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await sender(ctx, message)
    response = await client.wait_for("message", check=check, timeout=timeout)
    print(response.content)
    return response.content

async def sender(ctx, message: str):
    await ctx.channel.send(message)

#finnaly we have to run our bot. previous stuffs are defining the functions of the bot
client.run(TOKEN)