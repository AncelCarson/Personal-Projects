# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 2/3/2025
### Updated: 5/7/2025
### Windows 11
### Python command line, VSCode
### Server_Actions.py

"""A series of classes to manage specific server actions.

Each server will require different actions be performed. This module helps
organize those actions for clarity and consistency.

Classes:
    A_lot_to_do: Processes for the A Lot to do About Nothing server
    Berg_Barn: Processes for the Berg Barn
"""

# Libraries

# Object Class
class A_lot_to_do:
    """Actions for the A Lot to do About Nothing Server.
    
    Functions:
        raw_reaction:
        member_join:
    """
    @staticmethod
    async def raw_reaction(client, payload, guild: int) -> None:
        """Assigns a user role based on a reaction add.

        Parameters:
            client (bot): The BOt Instance that caught the reaction add
            payload (obj): The message package
            guild (int): The server ID
        """
        user = payload.user_id
        reaction = payload.emoji
        channel = client.get_channel(1326406285695909952)
        message = await channel.fetch_message(1345846363992100895)
        if payload.message_id == message.id: #this is a dm message
            guild = client.get_guild(guild)
            knows = guild.get_role(1326406775137767547)
            dontKnow = guild.get_role(1326406931300093982)
            member = guild.get_member(user)
            if str(reaction) == '\U0001F1FE':
                await member.add_roles(knows, reason="Preference Set")
                await member.remove_roles(dontKnow)
            if str(reaction) == '\U0001F1F3':
                await member.kick(reason = "They didn't make the cut")

    @staticmethod
    async def member_join(member, guild: int) -> None:
        """Assigns a role to a new user.

        Parameters:
            member (obj): Discord member object
        """

class Berg_Barn:
    """Actions for the A Lot to do About Nothing Server.
    
    Functions:
        member_join: Handles role assignemtn on a new member joining the server
    """
    @staticmethod
    async def member_join(member, title: str, guild: int) -> None:
        """Assigns a role to a new user.

        Parameters:
            member (obj): Discord member object
            title (str): a user's honorofic
            guild (int): The server ID
        """
        Madam = guild.get_role(1061842851220160664)
        Monsieur = guild.get_role(1061842845981491221)
        if title == "Sir":
            await member.add_roles(Monsieur, reason="Preference Set")
        elif title == "Madam":
            await member.add_roles(Madam, reason="Preference Set")
        await member.dm_channel.send("Your roles in Berg Barn have been updated")
