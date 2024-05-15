### Ancel Carson
### Created: 8/1/2023
### UPdated: 25/1/2023
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
    guild = discord.utils.get(client.guilds, id=GUILD)
    greeting = day_greeting()
    await member.create_dm()
    await member.dm_channel.send(f'Good {greeting[0]} {member.name}, welcome to {guild.name}')
    msg = await member.dm_channel.send("Please react below weather you are Male 'M' or Female 'F'")
    await msg.add_reaction('\U0001F1F2') #M
    await msg.add_reaction('\U0001F1EB') #F

#================   On Message      ================
@client.event
async def on_message(message):
    # Check that Jeeves does nto respond to his own message. 
    if message.author.id == client.user.id:
        return

    # Get user article
    # for role in message.author.roles:
    #     if role.id == 1061842845981491221: title = "Sir"
    #     elif role.id == 1061842851220160664: title = "Madam"
    #     else: title = "...you"

    # #get time article
    # greeting = day_greeting()

    if message.author.id not in activeUsers:
        activeUsers.append(message.author.id)
        activeThreads.append(TextHandler(sender, response_get))

    await activeThreads[activeUsers.index(message.author.id)].messageIn(message)

    #message starts with hi or hello then print these
    # if message.content[0] == '/':
    #     content = message.content.split(' ')

    #     if content[0] == "/Jeeves":
    #         # await message.delete()
    #         await message.channel.send("Good {1} {0}. {2}".format(title, greeting[0], greeting[1]))
    #         await message.channel.send("Good {1} {0}. {2}".format(title, greeting[0], greeting[1]))
    #         return


    #     if content[0] == "/DM":
    #         guild = client.get_guild(GUILD)
    #         member = message.author
    #         await member.create_dm()
    #         await member.dm_channel.send(f'good {greeting[0]} {member.name}, welcome to {guild.name}')
    #         msg = await member.dm_channel.send("Please react below weather you are Male 'M' or Female 'F'")
    #         await msg.add_reaction('\U0001F1F2') #M
    #         await msg.add_reaction('\U0001F1EB') #F

    #     if content[0] == "/Response":
    #         try:
    #             message1 = await response_get(message,"Say Something",60)
    #         except asyncio.TimeoutError:
    #             await message.channel.send("Oops too slow")
    #         else:
    #             await message.channel.send("You said {}".format(message1))


    if message.content.startswith('Bot Check'):
        await message.channel.send('Hello {0.author.mention} Bot is Running'.format(message))
        await message.channel.send('Jeeves is awaiting your command.')
    #when the message with help then do this

#================   Non Event Functions      ================
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

async def response_get(ctx, message: str,timeout: float):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await sender(message)
    response = await client.wait_for("message", check=check, timeout=timeout)
    print(response.content)
    return response.content

async def sender(ctx, message: str):
    await ctx.channel.send(message)


#finnaly we have to run our bot. previous stuffs are defining the functions of the bot
client.run(TOKEN)