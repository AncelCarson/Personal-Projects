# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 2/7/2025
### Updated: 3/7/2025
### Windows 11
### Python command line, VSCode
### User_Processor.py

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
import os
import uuid
import pandas as pd

# Variables
userFile = os.path.join(os.path.dirname(__file__), "users.csv")

# Object Class
class User_Processor():
    """Class Docstring.

    Attributes:
        fileLock (bool): The current state of the user file locked/unlocked (Default = False)
    
    Functions:
        aboutYou:
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

    def aboutYou(self, content: str, handler, greeting: str) -> None:
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
        userKey = makeKey(self.handleIn,self.handleOut)
        title = getSex(self.handleIn,self.handleOut)
        self.handleOut(f'Thank you {title} for answering my questions. I will update your data')
        userID = self.addUser(name, title, userKey)
        self.addInterface(userID, handler.userId, self.interface)
        self.handleOut('Close Thread!:!Your data has been stored')

    def addUser(self, name: str, title: str, userKey: str) -> str:
        """Adds a new ueser to the user file"""
        first,last = name.split(" ")
        userID = str(uuid.uuid4())
        newRow = {'UUID':userID, 'First_Name': first, 'Last_Name': last,
                  'Title': title, 'User_Key': userKey}
        while User_Processor.fileLock is True:
            pass
        User_Processor.fileLock = True
        userdf = pd.read_csv(userFile,dtype=str)
        userdf = pd.concat([userdf, pd.DataFrame([newRow])], ignore_index=True)
        userdf.to_csv(userFile, index=False)
        User_Processor.fileLock = False
        return userID

    def addInterface(self, userID: str, newID: str, interface: str) -> None:
        """Adds a new Interface for a user in the user file"""
        while User_Processor.fileLock is True:
            pass
        User_Processor.fileLock = True
        userdf = pd.read_csv(userFile, dtype=str)
        userdf.loc[userdf['UUID'] == userID, interface] = newID
        userdf.to_csv(userFile, index=False)
        User_Processor.fileLock = False


def makeKey(handleIn, handleOut) -> str:
    """Prompts the user for a Key Code"""
    userKey = handleIn('What would you like your unique Key Code to be? '\
                       'This code can be anything as long as you remember it.')
    handleOut(f'To verify, you have selected the following:\n> {userKey}')
    selection = handleIn('Is this correct? (Y/N)').upper()
    if selection == "Y":
        return userKey
    return makeKey(handleIn, handleOut)

def getID(interfaceID: str, interface: str) -> str:
    """Returns a user's unique ID based on an interface ID"""
    userdf = pd.read_csv(userFile, dtype=str)
    try:
        userID = userdf.loc[userdf[interface] == interfaceID, 'UUID'].item()
    except ValueError:
        userID = None
        print(f"UUID Error: {interface} ID {interfaceID} is not in the user file")
    return userID

def getTitle(userID: str) -> str:
    """Gets a user's title based off their ID"""
    userdf = pd.read_csv(userFile, dtype=str)
    try:
        title = userdf.loc[userdf['UUID'] == userID, 'Title'].item()
    except ValueError:
        title = "...you"
        print(f"Title Error: UUID {userID} is not in the user file")
    return title

def getName(userID: str) -> str:
    """Gets a user's name based on their ID and an interface"""
    userdf = pd.read_csv(userFile, dtype=str)
    try:
        name = userdf.loc[userdf['UUID'] == userID, 'First_Name'].item()
    except ValueError:
        name = "...you"
        print(f"Name Error: UUID {userID} is not in the user file")
    return name

def checkName(name: str) -> str|None:
    """Checks if a name exists inside of the user file. Returns the UserID if it does"""
    userdf = pd.read_csv(userFile, dtype=str)
    first,last = name.split(" ")
    users = userdf.loc[(userdf['First_Name'] == first) &
                        (userdf['Last_Name'] == last),
                        'UUID'].values
    if len(users) == 0:
        users = None
    return users

def checkKey(name: str, userKey: str) -> str|None:
    """Checks is a user's name and key match. If it does, it passes the UserID"""
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

def getSex(handleIn, handleOut) -> str:
    """Runs a loop to get a user's sex in case the input is not correct """
    handleOut("Are you Male (M) or Female (F)?")
    selection = handleIn("Please answer with a single Character").upper()
    if selection not in ['M','F']:
        handleOut("I do appologize, that is not the type of answer I was looking for.")
        handleOut("Please enter the single character")
        return getSex(handleIn, handleOut)
    return "Sir" if selection == "M" else "Madam"
