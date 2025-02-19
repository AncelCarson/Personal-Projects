# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 12/3/2023
### Updated: 18/3/2023
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
   performOperation: Does math to a set of rolls
   menu: The list of available options
"""

# Libraries
from re import search
from numpy.random import randint as rn

# Main Function
def main():
   """Driver of the program"""
   while True:
      diceRoll = input("What should I Roll?\n")
      if diceRoll.lower() in ["stop","exit"]:
         break
      diceRoll = diceRoll.split(" ")
      output = roller(diceRoll)
      print(output)
      # for line in output:
      #    print(line)

def roller(request: str):
   """Takes in the user request and breaks it into commands to be run.
   
   Parameters:
      request: Rolls the user wants to see

   Returns:
      outputStack: A string to show the steps the program took
   """
   request = wordCheck(request)
   total = 0
   count = 0
   first = True
   mathIt = False
   operation = "+"
   outputStack = ''
   newOperation = "+"
   request.append("@")

   # pylint: disable=used-before-assignment
   actionDict = {
      "drh": lambda line: (
         [0] if int(line[3:]) >= len(rolls)
         else dropHigh(rolls, int(line[3:]))
      ),
      "dr": lambda line: (
         [0] if int(line[2:]) >= len(rolls)
         else dropLow(rolls, int(line[2:]))
      ),
      "ei": lambda line: bigExplode(rolls, int(line[2:]), die, 0),
      "e": lambda line: explode(rolls, int(line[1:]), die),
      "kl": lambda line: (
         dropHigh(rolls, len(rolls) - int(line[2:])) if (len(rolls) - int(line[2:])) > 0
         else rolls
      ),
      "k": lambda line: (
         dropLow(rolls, len(rolls) - int(line[1:])) if (len(rolls) - int(line[1:])) > 0
         else rolls
      ),
      "ma": lambda line: reroll(rolls, int(line[2:]), die, "above"),
      "mi": lambda line: reroll(rolls, int(line[2:]), die, "below"),
      "ri": lambda line: rerollInf(rolls, int(line[2:]), die, "same"),
      "r": lambda line: reroll(rolls, int(line[1:]), die, "same"),
      "mai": lambda line: rerollInf(rolls, int(line[3:]), die, "above"),
      "mii": lambda line: rerollInf(rolls, int(line[3:]), die, "below"),
   }
   # pylint: enable=used-before-assignment

   while count < len(request):
      line = request[count]
      action = search(r'\D+', line).group(0).lower() if search(r'\D+', line) else " "
      count += 1
      if line.lower() in ("help","h"):
         return menu()
      if line == "@":
         mathIt = True
      elif action in actionDict:
         rolls = actionDict[action](line)
         outputStack += f"{rolls}\n"
      elif "d" in line:          #Dice to Roll
         [rolls,die] = roll(*line.split('d'))#Dice Results
         outputStack += f"{rolls}\n"
         # outputStack.append(list(rolls))
      elif line in ["+","-","/","*"]:
                                 #Operation Request
         newOperation = line     #Saves Operation Request
         mathIt = True           #signifies the next item will need to be calculated
      else:
         if first:
            commands = request[1:]
            request.extend(command for _ in range(int(line) - 1) for command in commands)
         else:
            rolls = [int(line)]
            outputStack += f"{int(line)}\n"

      if mathIt:
         rollTotal = sum(rolls)
         total = performOperation(total, rollTotal, operation)
         outputStack += f"{total}\n"
         operation = newOperation
         if line == "@":
            total = 0
            operation = "+"
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

def performOperation(total: float, rollTotal: int, operation: str):
   """Performs mathmatical operations between different rolls or numbers.
   
   Parameters:
      total: Overall total from the start of the loop
      rollTotal: The sum of the most recent roll
      operation: Which mathmaatical operation is being performed

   Returns:
      total: An updated overall total from the start of the loop
   """
   if operation == "-":
      return total - rollTotal
   if operation == "/":
      return total if rollTotal == 0 else total / rollTotal
   if operation == "*":
      return total * rollTotal
   return total + rollTotal

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
