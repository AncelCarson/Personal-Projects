# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 12/3/2023
### UPdated: 12/3/2023
### Windows 11
### Python command line, VS Code, IDLE
### Roller.py

"""A random number generator given dice rolls.

This program asks the user for a selection of dice to be rolled and a series
of actions to perform on that roll. It then generates the numbers, performs
said action, and displays the results. 

Example:
   6 4d6 r1 dr1 will give the folloing actions:
   -> 4 "dice" will be rolled with a integer range of 1 - 6.
   -> If there are any 1s in that list of rolls, they will be rerolled.
   -> If the lowest die will then be dropped from the list.
   -> This will be repeated 5 more times for a tital of 6 sets of rolls.

Methods:
   main: Driver of the program
   roller: Text parser and processor
   wordCheck: Checks for keywords
   roll: "Rolls" the dice giving a list of random numbers based on user input
   dropLow: Removes a certain number of the lowest rolls from the list
   dropHigh: Removes a certain number of the hignest rolls from the list
   explode: Rerolls a die if the maximum number is rolled
   bigExplode: Infinitely rerolls a die if the maximum number is rolled
   reroll: Generates a new roll based on given criteria
   rerollInf: Infinitely generates a new roll based on given criteria
   menu: The list of available options
"""

# Libraries
from numpy.random import randint as rn

# Main Function
def main():
   """Driver of the program"""
   while True:
      diceRoll = input("What should I Roll?\n")
      if diceRoll == "Stats":
         diceRoll = "6 4d6 r1 dr1"
      diceRoll = diceRoll.split(" ")
      output = roller(diceRoll)
      print(output)
      # for line in output:
      #    print(line)

def roller(request: str):
   """Takes in the user request and breaks it into commands to be run.
   
   Parameters:
      request: Rolls the user wants to see

   Variables:
      total (int): Final Result to Return
      count (int): Current loop iteration number
      first (bool): Verifies if this is the First Iteration
      mathIt (bool): Calculate Rolls Together
      rolling (bool): Main foor loop when rolling or modifying the roll list
      operation (char): Operation to Perform in Calculation Addition first to sum first roll set
      outputStack (list -> str): A list of the action performend while rolling
      newOperation (char): Next operation to perform when combining sets of rolls

   Returns:
      outputStack
   """
   request = wordCheck(request)
   total = 0
   count = 0
   first = True
   mathIt = False
   rolling = True
   operation = "+"
   outputStack = ''
   newOperation = "+"
   request.append("@")
   while rolling:
      line = request[count]
      count += 1
      if count == len(request):
         rolling = False
      if line in ("help","Help","HELP","h","H"):
         return menu()
      if line == "@":
         mathIt = True
      elif "drh" in line:          #Drop the Highest Dice
         num = int(line[3:])
         if num == len(rolls):
            rolls = [0]
            continue
         rolls = dropHigh(rolls, num)
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif "dr" in line:         #Drop the Lowest Dice
         num = int(line[2:])
         if num == len(rolls):
            rolls = [0]
            continue
         rolls = dropLow(rolls, num)
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif "d" in line:          #Dice to Roll
         [num,die] = line.split('d')
         [rolls,die] = roll(num,die)#Dice Results
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
      elif "ei" in line:         #Explode Dice Infinitely
         num = int(line[2:])
         bigExplode(rolls, num, die, 0)
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif "e" in line:          #Explode Dice
         num = int(line[1:])
         explode(rolls, num, die)
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif "kl" in line:         #Keep the Lowest Dice
         num = len(rolls) - int(line[2:])
         if num == 0:
            continue
         rolls = dropHigh(rolls, num)
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif "k" in line:          #Keep the Highest Dice
         num = len(rolls) - int(line[1:])
         if num == 0:
            continue
         rolls = dropLow(rolls, num)
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif "ma" in line:          #Reroll any Die Above the Maximum
         num = int(line[2:])
         rolls = reroll(rolls, num, die, "above")
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif "mi" in line:          #Reroll any Die Below the Minimum
         num = int(line[2:])
         rolls = reroll(rolls, num, die, "below")
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif "ri" in line:          #Reroll any Die of a Certain Value
         num = int(line[2:])
         rolls = rerollInf(rolls, num, die, "same")
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif "r" in line:          #Reroll any Die of a Certain Value
         num = int(line[1:])
         rolls = reroll(rolls, num, die, "same")
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif "ima" in line:          #Reroll any Die Above the Maximum
         num = int(line[2:])
         rolls = rerollInf(rolls, num, die, "above")
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif "imi" in line:          #Reroll any Die Below the Minimum
         num = int(line[2:])
         rolls = rerollInf(rolls, num, die, "below")
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif line in ["+","-","/","*"]:
                                 #Operation Request
         newOperation = line    #Saves Operation Request
         mathIt = True           #signifies the next item will need to be calculated
      else:
         if first:
            commands = request[1:]
            for _ in range(int(line)-1):
               for command in commands:
                  request.append(command)
         else:
            rolls = [int(line)]
            outputStack += (str(int(line)) + "\n")
            # outputStack.append(list([int(line)]))

      if mathIt:
         rollTotal = 0
         for die in rolls:
            rollTotal += die
         if operation == "-":
            total = total - rollTotal
         elif operation == "/":
            if rollTotal == 0:
               pass
            else:
               total = total / rollTotal
         elif operation == "*":
            total = total * rollTotal
         else:
            total = total + rollTotal
         outputStack += (str(total) + "\n")
         # outputStack.append(int(total))
         operation = newOperation
         if line == "@":
            total = 0
         mathIt = False

      first = False              #Signifies the end of the First Loop
   return outputStack

def wordCheck(request: str):
   """Check for keywords and adjusts the input to match.

   Examples:
      Stats/stats -> 6 4d6 r1 dr1

   Parameters:
      request: User input

   Returns:
      request (list -> str): Set of actions broken into a list
   """
   if request[0] in ["Stats","stats"]:
      request = "6 4d6 r1 dr1".split(" ")
   else:
      pass
   return request

def roll(num: int, die: int):
   """Runs the random number generator based on rolls given.
   
   xdy rolls a y sided die x number of times

   Parameters:
      num: The number of rolls to make (x)
      die: The die to be rolled (y)

   Returns:
      rolls (list -> int):
      die: The die that was rolled
   """
   rolls = []
   for _ in range(int(num)):
      rolls.append(rn(1, high = int(die)+1))
   return [rolls,die]

def dropLow(rolls: list[int], num: int):
   """Drops the lowest value in the list of rolls based on a given number.
   
   Parameters:
      rolls: The list of rolls made
      num: The number of rolls to drop

   Returns:
      rolls: An updated list of the rolls made
   """
   for _ in range(num):
      rolls.remove(min(rolls))
   return rolls

def dropHigh(rolls: list[int], num: int):
   """Drops the highest value in the list of rolls based on a given number.
   
   Parameters:
      rolls: The list of rolls made
      num: The number of rolls to drop

   Returns:
      rolls: An updated list of the rolls made
   """
   for _ in range(num):
      rolls.remove(max(rolls))
   return rolls

def explode(rolls: list[int], num: int, die: int):
   """Rolls an additional die if it is the maximum possible number.
   
   Parameters:
      rolls: The list of rolls made
      num: The number of rolls to drop
      die: The die that was rolled

   Returns:
      rolls: An updated list of the rolls made
   """
   [newRolls,die] = roll(rolls.count(num),die)
   for value in newRolls:
      rolls.append(value)
   return rolls

def bigExplode(rolls: list[int], num: int, die: int, count: int):
   """Rolls an additional die if it is the maximum possible number recursively.
   
   Parameters:
      rolls: The list of rolls made
      num: The number of rolls to drop
      die: The die that was rolled
      count: The number of times the recusion has run

   Returns:
      rolls: An updated list of the rolls made
   """
   if count == 50:               #Maximum Recursion 50 Loops
      return rolls
   if rolls.count(num) > 0:
      [newRolls,die] = roll(rolls.count(num),die)
      newRolls = bigExplode(newRolls, num, die, count + 1)
   else:
      return rolls
   for value in newRolls:
      rolls.append(value)
   return rolls

def reroll(rolls: list[int], num: int, die: int, direction: str):
   """Rerolls any roll based on a certain citeria.
   
   Parameters:
      rolls: The list of rolls made
      num: The number of rolls to drop
      die: The value to check against
      direction: Control value for rolling anything above, below, or equal to the die 

   Returns:
      rolls: An updated list of the rolls made
   """
   for count, _ in enumerate(rolls):
      if direction == "above":
         if rolls[count] > num:
            [[rolls[count]],_] = roll(1, die)
      if direction == "below":
         if rolls[count] < num:
            [[rolls[count]],_] = roll(1, die)
      if direction == "same":
         if rolls[count] == num:
            [[rolls[count]],_] = roll(1, die)
   return rolls




def rerollInf(rolls: list[int], num: int, die: int, direction: str):
   """Rerolls any roll based on a certain citeria recursively.
   
   Parameters:
      rolls: The list of rolls made
      num: The number of rolls to drop
      die: The value to check against
      direction: Control value for rolling anything above, below, or equal to the die 

   Returns:
      rolls: An updated list of the rolls made
   """
   deeper = False
   for count, _ in enumerate(rolls):
      if direction == "above":
         if rolls[count] > num:
            [[rolls[count]],_] = roll(1, die)
            deeper = True
      if direction == "below":
         if rolls[count] < num:
            [[rolls[count]],_] = roll(1, die)
            deeper = True
      if direction == "same":
         if rolls[count] == num:
            [[rolls[count]],_] = roll(1, die)
            deeper = True
   if deeper:
      rolls = rerollInf(rolls, num, die, direction)
   return rolls

# def menu():
#    return[["|               Command Menu               |"],
#     ["|------------------------------------------|"],
#     ["| xdy: Roll x number of y sided dice       |"],
#     ["| dr#: Drop # of lowest dice               |"],
#     ["|  k#: Keep # of highest dice              |"],
#     ["|drh#: Drop # of highest dice              |"],
#     ["|  e#: Explode dice of # once              |"],
#     ["| ei#: Explode dice of # infinitely        |"],
#     ["| ma#: Reroll any die above # once         |"],
#     ["| mi#: Reroll any die below # once         |"],
#     ["|  r#: Reroll any die equal to # once      |"],
#     ["|mai#: Reroll any die above # infinitely   |"],
#     ["|mii#: Reroll any die below # infinitely   |"],
#     ["| ri#: Reroll any die equal to # infinitely|"],
#     ["|help: Show this menu                      |"],
#     ["|------------------------------------------|"],]

def menu():
   """List of available roll actions"""
   return"""Command Menu
---------------------
xdy:\tRoll x number of y sided dice
dr#:\tDrop # of lowest dice
k#:\tKeep # of highest dice
drh#:\tDrop # of highest dice
e#:\tExplode dice of # once
ei#:\tExplode dice of # infinitely
ma#:\tReroll any die above # once
mi#:\tReroll any die below # once
r#:\tReroll any die equal to # once
mai#:\tReroll any die above # infinitely
mii#:\tReroll any die below # infinitely
ri#:\tReroll any die equal to # infinitely
help:\tShow this menu
---------------------"""

# Self Program Call
if __name__ == '__main__':
   main()
