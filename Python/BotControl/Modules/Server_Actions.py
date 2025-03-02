# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 2/3/2025
### Updated: 2/3/2025
### Windows 11
### Python command line, VSCode
### Server_Actions.py

"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Classes:
    A_lot_to_do:
"""

# Libraries

# Object Class
class A_lot_to_do:
    """Class Docstring.
    
    Functions:
        raw_reaction:
        member_join:
    """
    @staticmethod
    async def raw_reaction(client, payload, guild):
        """Function Docstring.

        Parameters:
            self (self): Ths instance of this class 

        Returns:
            None (none_type): This is an example
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
    async def member_join(client, member, guild):
        """Function Docstring.

        Parameters:
            self (self): Ths instance of this class 

        Returns:
            None (none_type): This is an example
        """
