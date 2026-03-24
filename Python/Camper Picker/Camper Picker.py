# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### 3/8/2020
### Windows 10
### Python command line, Notepad, VSCode

# Libraries
import pandas as pd
import random as rand
import pyodbc

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\ancel\OneDrive\Documents\Coding\Python\Camper Picker\CampChowabunga.mdb;'
    )
cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()

# Global variables
day = 0
campers = []
parties = []
baseCamp = []
camp = True

# Main Function
def main():
    setKids()
    assignParties()
    newDay = input("Does the session start on a new day?\n")
    if newDay == "no":
        pass
    else:
        startDay()
    menu(1)
    campStart()

# Secondary Function that handles opperations
def campStart():
    global camp, campers, baseCamp
    while camp == True:
        command = input("\nenter a command\n")
        if command == 'add':
            print("Which campers do you want to add?")
            getCommand = input("type menu for instructions\n")
            if getCommand == 'random':
                randomPicker()
            elif getCommand == 'select':
                addCamper()
            elif getCommand == 'menu':
                menu(2)
        elif command == 'get':
            showCamper()
        elif command == 'show':
            showParty()
        elif command == 'home':
            partyHome()
        elif command == 'fight':
            startFight()
        elif command == 'morning':
            startDay()
            print("All living camper's hp reset")
        elif command == 'day':
            getDay()
        elif command == 'revive':
            reviveCamper(baseCamp)
        elif command == 'menu':
            menu(1)
        elif command == 'end':
            print('Camp is now over, ending program\n')
            sendKids()
            input("Press enter to end program")
            camp = False
        elif command == 'basecamp':
            displayGroup(baseCamp)

# Adds a number of selected campers to a new or existing group
def addCamper():
    global parties, campers
    party = []
    newParty = input("Do you want to make a new party?\n")
    if newParty == 'yes':
        party = makeParty()
    elif newParty == 'no':
        print("There are %s parties out" % len(parties))
        if len(parties) == 0:
            print("There must be at least one party")
            return
        partySelect = int(input("Which one do you want to add to?\n"))
        party = parties[partySelect - 1]
    numAdd = int(input("How many campers do you want to add?\n"))
    if numAdd > len(campers):
        print("You cannot add more campers than those at basecamp")
        return
    print("Avaliable campers")
    displayGroup(campers)
    for num in range(numAdd):
        camperName = input("Who do you want to add?\n")
        for camper in campers:
            if camper[1] == camperName:
                movedCamper = campers.pop(campers.index(camper))
                party.append(movedCamper)
                break

# Assignes campers to the party of the previous session
def assignParties():
    global parties, campers, day
    for row in cursor.execute("SELECT Parties, Day FROM Camp_Data;"):
        numParties = row[0]
        day = row[1]
    if numParties != 0:
        for num in range(numParties):
            makeParty()
        for camper in baseCamp:
            if camper[8] != 0:
                movedCamper = campers.pop(campers.index(camper))
                parties[camper[8] - 1].append(movedCamper)
            camper[8] = 0

# Displays the camper in a given party
def displayGroup(group):
    for camper in group:
        print("%s, %s   \tspecializing in %s,   \thealth %s" % (camper[1], camper[5], camper[2], camper[4]))

# Displays the day of the week
def getDay():
    global day
    switcher = {
        1: 'Sunday',
        2: 'Monday',
        3: 'Tuesday',
        4: 'Wednesday',
        5: 'Thursday',
        6: 'Friday',
        7: 'Saturday'
    }
    print(switcher.get(day))

# Harms a camper in a given group or all campers in a group
def harmCamper(group):
    fightCommand = input("Who was damaged?\n")
    if fightCommand == 'all':
        damage = int(input("How much damage?\n"))
        for camper in group:
            camper[4] = camper[4] - damage
            if camper[4] <= 0:
                print("%s is down" % camper[1])
                camper[4] = 0
                camper[6] = False
            print("%s has %s hp" % (camper[1], camper[4]))
    else:
        for camper in group:
            if camper[1] == fightCommand:
                damage = int(input("How much damage?\n"))
                camper[4] = camper[4] - damage
                if camper[4] <= 0:
                    print("%s is down" % camper[1])
                    camper[4] = 0
                    camper[6] = False
                print("%s has %s hp" % (camper[1], camper[4]))
                break

# Checks the heats of all campers in a given group
def healthCheck(group):
    for camper in group:
        print("%s has %s hp" % (camper[1], camper[4]))
        if camper[6] == False:
            print("%s is down" % camper[1])

# Makes a new party and adds it to the group of parties
def makeParty():
    global parties 
    parties.append([])
    return parties[len(parties)-1]

# Contains all menues used by the program
def menu(menuNum):
    if menuNum == 1:
        print("|-----------------------------|")
        print("|add - recieve campers        |")
        print("|get - shows random campers   |")
        print("|show - shows camper party    |")
        print("|home - return campers to camp|")
        print("|fight - start combat         |")
        print("|morning - reset camper hp    |")
        print("|day - get the day of the week|")
        print("|revive - revives a camper    |")
        print("|menu - opens this menu       |")
        print("|end - ends progeam           |")
        print("|-----------------------------|")
    elif menuNum == 2:
        print("|-----------------------------|")
        print("|random - picks random campers|")
        print("|select - add specific campers|")
        print("|-----------------------------|")

# Returns a party of campers to camp and removes the party from parties
def partyHome():
    global parties, campers
    print("There are %s parties out" % len(parties))
    homeSelect = input("Which one do you want to send home?\n")
    if homeSelect == 'all':
        for num1 in range(len(parties)):
            for num2 in range(len(parties[0])):
                camper = parties[0].pop(0)
                campers.append(camper)
            parties.pop(0)
    else:
        homeSelect = int(homeSelect)
        for num in range(len(parties[homeSelect - 1])):
            camper = parties[homeSelect - 1].pop(0)
            campers.append(camper)
        parties.pop(homeSelect - 1)

# Selects a number of random campers for a party
def randomPicker():
    global parties, campers
    party = []
    newParty = input("Do you want to make a new party?\n")
    if newParty == 'yes':
        party = makeParty()
    elif newParty == 'no':
        print("There are %s parties out" % len(parties))
        if len(parties) == 0:
            print("There must be at least one party")
            return
        partySelect = int(input("Which one do you want to add to?\n"))
        party = parties[partySelect - 1]
    numRand = int(input('How many campers do you want?\n'))
    if numRand > len(campers):
        print("You cannot add more campers than those at basecamp")
        return
    for num in range(numRand):
        camper = campers.pop(rand.randint(0,len(campers) - 1))
        party.append(camper)

# Revives an unconcious camper
def reviveCamper(group):
    camperHeal = input("Who is being revived?\n")
    for camper in group:
        if camper[1] == camperHeal:
            camper[6] = True
            heal = int(input("How much were they healed?\n"))
            camper[4] = camper[4] + heal
            print("%s has %s hp" % (camper[1], camper[4]))

# Updates database after program is finished
def sendKids():
    global baseCamp, day
    for party in range(len(parties)):
        for camper in parties[party]:
            camper[8] = party + 1
    for camper in baseCamp:
        cursor.execute("UPDATE [Campers] SET AC = ?, HP = ?, Alive = ?, Party = ? WHERE Camper = ?;",\
            camper[3], str(camper[4]), camper[6], camper[8], camper[1])
    cursor.execute("UPDATE [Camp_Data] SET Parties = ?, Day = ? WHERE ID = ?;", len(parties), day, 1)
    cnxn.commit()
    cursor.close()
    cnxn.close()

# Pulls camper data from database
def setKids():
    global campers, baseCamp
    for row in cursor.execute("SELECT * FROM Campers;"):
        campers.append(row)
        baseCamp.append(row)

# Shows a random group of campers
def showCamper():
    global campers, baseCamp
    party = []
    showCommand = input("Do you want campers from camp or basecamp?\n")
    camperNum = int(input("How many campers do you want?\n"))
    if showCommand == 'camp':
        group = campers
    elif showCommand == 'basecamp':
        group = baseCamp
    for num in range(camperNum):
        camper = group.pop(rand.randint(0,len(group) - 1))
        party.append(camper)
    displayGroup(party)
    for num in range(len(party)):
            camper = party.pop(0)
            group.append(camper)

# Displays camper information for party of camp
def showParty():
    global parties, campers, baseCamp
    print("There are %s parties and %s campers at basecamp" % (len(parties), len(campers)))
    showCommand = input("do you want to check camp or a party?\n")
    if showCommand == 'camp':
        displayGroup(campers)
    elif showCommand == 'basecamp':
        displayGroup(baseCamp)
    elif showCommand == 'party':
        if len(parties) == 0:
            print("There are no parties out")
            return
        partySelect = int(input("Which party do you want to check?\n"))
        if partySelect > len(parties):
            print("This party does not exist")
            return
        elif partySelect <= 0:
            print("Choice must be a positive non 0 integer")
        displayGroup(parties[partySelect - 1])

# Heals all campers who are at camp
def startDay():
    global day
    for camper in campers:
        if camper[6] == True:
            camper[4] = camper[7]
    if day == 7:
        day = 1
    else:
        day += 1

# Handles fights where campers may be harmed
def startFight():
    global parties
    fight = True
    print("There are %s parties out" % len(parties))
    activeParty = int(input("Which party is in combat?\n"))
    print("Active combatants")
    displayGroup(parties[activeParty - 1])
    while(fight):
        fightCommand = input("Would you like to harm, heal or check?\n")
        if fightCommand == 'harm':
            harmCamper(parties[activeParty - 1])
        elif fightCommand == 'heal':
            reviveCamper(parties[activeParty - 1])
        elif fightCommand == 'check':
            healthCheck(parties[activeParty - 1])
        elif fightCommand == 'change':
            print("There are %s parties out" % len(parties))
            newParty = int(input("Which party is in combat?\n"))
            if newParty <= 0:
                print("Party must exist, No change made")
            elif newParty > len(parties):
                print("Party must exist, No change made")
            else:
                activeParty = newParty
        elif fightCommand == 'end':
            fight = False

# Self Program Call
if __name__ == '__main__':
    main()
