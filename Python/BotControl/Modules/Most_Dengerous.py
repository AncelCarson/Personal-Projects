# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 14/3/2026
### Updated: 15/3/2026
### Windows 11/Ubuntu Linux
### Python command line, VSCode
### MOst_Dangerous.py

"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Classes:
    Character:

Functions:
   main: Driver of the program
"""

# Libraries
from Roller import straightRoll as roll

# Global Variables

# Object Class
class Character():
    """Class Docstring.

    Attributes:
        userID (str): User ID of the player
        gameID (str): ID of the game this character is playing in
        name (str): Name of the Character
        stats (List -> int): List of numerical stats of the character:
            Str, Dex, Con, Int, Wis, Cha, Speed, Health
        location (str): Current location of the Character
        Tools (List -> obj): List of tools that a Character has access to
    
    Functions:
        setName:
        setStats:
        rollStats:
        getStats:
    """
    def __init__(self,userID=None, gameID=None):
        self.userID = userID
        self.gameID = gameID
        self.name = None
        self.stats = [10,10,10,10,10,10,1,10]
        self.location = "A1"
        self.tools = None

    def __enter__(self):
        #TODO: Needed?
        pass

    def __exit__(self, *exc):
        #TODO: Needed?
        pass

    def setName(self, name):
        """Sets the name of a Character"""
        self.name = name

    def setStats(self, stats):
        """Sets the stats of a Character"""
        self.stats = stats

    def rollStats(self):
        """Generates stats for a character"""

    def getStat(self, statCode: int) -> int:
        """Returns the specified stat of a Character"""
        return self.stats[statCode]


class Game():
    """Class Docstring.

    Attributes:
        location (str): Originating location of the current game
        gameID (str): ID of the game that is running
        round (int): Current round of the game
    
    Functions:
        setName:
        setStats:
        rollStats:
        getStats:
    """

    def __init__(self,location=None):
        self.location = location
        self.gameID = None
        self.round = 0

    def __call__(self):
        # Add actions on class call. Maybe start game?
        pass

    def __enter__(self):
        pass

    def __exit__(self, *exc):
        pass

    def start(self):
        """Function Docstring."""


# Main Function
def main():
    """Function Docstring."""
    game = Game(location="Admin Panel")
    game.start()

# Self Program Call
if __name__ == '__main__':
    print(roll("4d6 r1 dr1"))
    # main()
