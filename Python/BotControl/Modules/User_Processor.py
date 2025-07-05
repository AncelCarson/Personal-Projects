# pylint: disable=invalid-name,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 2/7/2025
### Updated: 5/7/2025
### Windows 11
### Python command line, VSCode
### User_Processor.py

"""User data processor for Jeeves.

This module handles the access to the user data files. It takes in requests,
returns the required data, and will lock out the file if it is used in another
process. 

Classes:
    User_Processor: Class to handle the writing to the user file

Functions:
   checkKey: Checks to find that a user exists using name and user key
   checkName: Checks to find that a user exists using name and user key
   getID: Returns a user's ID based on the interface ID
   getName: Returns a user's name based on their UserID
   getPermission: Returns a user's permission level based on their UserID
   getTitle: Returns a user's title based on their UserID

Parameters:
    userFile (str): The location of the user file
"""

# Libraries
import os
import uuid
import pandas as pd

# Variables
userFile = os.path.join(os.path.dirname(__file__), "users.csv")

# Object Class
class User_Processor():
    """Handles the creation of new users and writing to the user file.

    Attributes:
        fileLock (bool): The current state of the user file locked/unlocked (Default = False)

    Functions:
        aboutYou: Runs the user setup process
        addUser: Adds a new user to the user file
        addInterface: Adds an interface ID for an existing user
    """

    fileLock = False

    def __init__(self, interface="cmd", handleIn=None, handleOut=None):
        self.interface = interface
        self.handleIn = handleIn
        self.handleOut = handleOut

    def __call__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, *exc):
        pass

    def aboutYou(self, content: str, handler: object, greeting: str) -> None:
        """Tests the Response processing of the text handler.

        Parameters:
            content (str): Message from the user
            handler (TextHandler): Object for the current Thread
            greeting (str): Message from the TextHandler for the time of day
        """
        if len(content) == 1:
            content.append(handler.userId)
        handler.mode = "userSetTest"
        self.handleOut(f'Good {greeting}. I am here to assist you')
        name = self.handleIn("Would you please tell me your First and Last Name?")
        if checkName(name) is not None:
            self.handleOut('It appears I have that name in my system')
            self.handleOut('Will you please enter your user key for verification?')
            userKey = self.handleIn('If you have no user key, simply enter "None"')
            userID = checkKey(name, userKey)
            if userID is not None:
                self.handleOut(f'Wonderful to see you again {getTitle(userID)}')
                self.handleOut('I will add this interface to my records for future reference')
                self.addInterface(userID, handler.userId, self.interface)
                self.handleOut('Close Thread!:!Your data has been stored')
                return
        self.handleOut('We will now want to create a unique Key Code for yourself')
        userKey = _makeKey(self.handleIn,self.handleOut)
        title = _getSex(self.handleIn,self.handleOut)
        self.handleOut(f'Thank you {title} for answering my questions. I will update your data')
        userID = self.addUser(name, title, userKey)
        self.addInterface(userID, handler.userId, self.interface)
        self.handleOut('Close Thread!:!Your data has been stored')

    def addUser(self, name: str, title: str, userKey: str) -> str:
        """Adds a new user to the user file

        Parameters:
            name (str): A user's first and last name
            title (str): A user's honorific
            userKey (str): A user's chosen passphrase

        Returns:
            userID (str): A users unique ID
        """
        first,last = name.split(" ")
        userID = str(uuid.uuid4())
        newRow = {'UUID':userID, 'First_Name': first, 'Last_Name': last,
                  'Title': title, 'User_Key': userKey, 'Permission': "User"}
        while User_Processor.fileLock is True:
            pass
        User_Processor.fileLock = True
        userdf = pd.read_csv(userFile,dtype=str)
        userdf = pd.concat([userdf, pd.DataFrame([newRow])], ignore_index=True)
        userdf.to_csv(userFile, index=False)
        User_Processor.fileLock = False
        return userID

    def addInterface(self, userID: str, newID: str, interface: str) -> None:
        """Adds a new Interface for a user in the user file

        Parameters:
            userID (str): A users unique ID
            newID (str): An ID being added from a new interface
            interface (str): The source of the user input
        """
        while User_Processor.fileLock is True:
            pass
        User_Processor.fileLock = True
        userdf = pd.read_csv(userFile, dtype=str)
        userdf.loc[userdf['UUID'] == userID, interface] = newID
        userdf.to_csv(userFile, index=False)
        User_Processor.fileLock = False


def checkKey(name: str, userKey: str) -> str|None:
    """Checks is a user's name and key match. If it does, it passes the UserID

    Parameters:
        name (str): A user's first and last name
        userKey (str): A user's chosen passphrase

    Returns:
        userID (str|None): A users unique ID or None if no user was found
    """
    userdf = pd.read_csv(userFile, dtype=str)
    first,last = name.split(" ")
    try:
        userID = userdf.loc[(userdf['First_Name'] == first) &
                            (userdf['Last_Name'] == last) &
                            (userdf['User_Key'] == userKey),
                            'UUID'].item()
    except ValueError:
        userID = None
    return userID

def checkName(name: str) -> str|None:
    """Checks if a name exists inside of the user file. Returns the UserID if it does

    Parameters:
        name (str): A user's first and last name

    Returns:
        userID (str|None): A list of users with a certain name or None if no user was found
    """
    userdf = pd.read_csv(userFile, dtype=str)
    first,last = name.split(" ")
    users = userdf.loc[(userdf['First_Name'] == first) &
                        (userdf['Last_Name'] == last),
                        'UUID'].values
    if len(users) == 0:
        users = None
    return users

def getID(interfaceID: str, interface: str) -> str:
    """Returns a user's unique ID based on an interface ID

    Parameters:
        interfaceID (str): A users ID from a specific interface
        interface (str): The source of the user input

    Returns:
        userID (str): A users unique ID
    """
    userdf = pd.read_csv(userFile, dtype=str)
    try:
        userID = userdf.loc[userdf[interface] == interfaceID, 'UUID'].item()
    except ValueError:
        userID = None
        print(f"UUID Error: {interface} ID {interfaceID} is not in the user file")
    return userID

def getName(userID: str) -> str:
    """Gets a user's name based on their ID and an interface

    Parameters:
        userID (str): A users unique ID

    Returns:
        name (str): A user's first name
    """
    userdf = pd.read_csv(userFile, dtype=str)
    try:
        name = userdf.loc[userdf['UUID'] == userID, 'First_Name'].item()
    except ValueError:
        name = "...you"
        print(f"Name Error: UUID {userID} is not in the user file")
    return name

def getPermission(userID: str) -> str:
    """Returns a users permission level given their UserID

    Parameters:
        userID (str): A users unique ID

    Returns:
        permission (str): A user's permission level
    """
    userdf = pd.read_csv(userFile, dtype=str)
    try:
        permission = userdf.loc[userdf['UUID'] == userID, 'Permission'].item()
    except ValueError:
        permission = "User"
        print(f"Permission Error: UUID {userID} is not in the user file")
    return permission

def getTitle(userID: str) -> str:
    """Gets a user's title based off their ID

    Parameters:
        userID (str): A users unique ID

    Returns:
        title (str): A user's honorific
    """
    userdf = pd.read_csv(userFile, dtype=str)
    try:
        title = userdf.loc[userdf['UUID'] == userID, 'Title'].item()
    except ValueError:
        title = "...you"
        print(f"Title Error: UUID {userID} is not in the user file")
    return title

def _getSex(handleIn: object, handleOut: object) -> str:
    """Runs a loop to get a user's sex in case the input is not correct
    
    Parameters:
        handleIn (queue): Custom input() method
        handleOut (queue): Custom output() method
    
    Returns:
        _ (str): "Sir" or "Madam"
    """
    handleOut("Are you Male (M) or Female (F)?")
    selection = handleIn("Please answer with a single Character").upper()
    if selection not in ['M','F']:
        handleOut("I do appologize, that is not the type of answer I was looking for.")
        handleOut("Please enter the single character")
        return _getSex(handleIn, handleOut)
    return "Sir" if selection == "M" else "Madam"

def _makeKey(handleIn: object, handleOut: object) -> str:
    """Prompts the user for a Key Code
    
    Parameters:
        handleIn (queue): Custom input() method
        handleOut (queue): Custom output() method
    
    Returns:
        userKey (str): userKey (str): A user's chosen passphrase
    """
    userKey = handleIn('What would you like your unique Key Code to be? '\
                       'This code can be anything as long as you remember it.')
    handleOut(f'To verify, you have selected the following:\n> {userKey}')
    selection = handleIn('Is this correct? (Y/N)').upper()
    if selection == "Y":
        return userKey
    return _makeKey(handleIn, handleOut)
