### Ancel Carson
### Created: 12/3/2023
### UPdated: 12/3/2023
### Windows 11
### Python command line, VS Code, IDLE
### Roller.py

# Libraries
from numpy.random import randint as rn

# Object Class
class Roller():
    def hello(self):
        print("Hello")

    def world(self):
        print("World")

# Main Function
def main():
   while(True):
      diceRoll = input("What should I Roll?\n")
      if diceRoll == "Stats":
         diceRoll = "6 4d6 r1 dr1"
      diceRoll = diceRoll.split(" ")
      output = roller(diceRoll)
      print(output)
      # for line in output:
      #    print(line)

def roller(input):
   input = wordCheck(input)
   total = 0                     #Final Result to Return
   count = 0
   first = True                  #Verifies if this is the First Iteration
   mathIt = False                #Calculate Rolls Together
   rolling = True
   operation = "+"               #Operation to Perform in Calculation Addition first to sum first roll set
   outputStack = ''              
   newOperation = "+"
   input.append("@")
   while rolling:
      line = input[count]
      count += 1
      if count == len(input):
         rolling = False
      if line == "help" or line == "Help" or line == "HELP" or line == "h" or line == "H":
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
      elif "ir" in line:          #Reroll any Die of a Certain Value
         num = int(line[1:])
         rolls = rerollInf(rolls, num, die, "same")
         outputStack += (str(rolls) + "\n")
         # outputStack.append(list(rolls))
         continue
      elif line in ["+","-","/","*"]:
                                 #Operation Request
         newOperation = line    #Saves Operation Request
         mathIt = True           #signifies the next item will need to be calculated
      else:
         if first:
            commands = input[1:]
            for _ in range(int(line)-1):
               for command in commands:
                  input.append(command)
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
               total = total
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

def wordCheck(input):
   if input[0] in ["Stats","stats"]:
      input = "6 4d6 r1 dr1".split(" ")
   else:
      pass
   return input

def roll(num, die):
   rolls = []
   for _ in range(int(num)):
      rolls.append(rn(1, high = (int(die)+1)))
   return [rolls,die]

def dropLow(rolls, num):
   for _ in range(num):
      rolls.remove(min(rolls))
   return rolls

def dropHigh(rolls, num):
   for _ in range(num):
      rolls.remove(max(rolls))
   return rolls

def explode(rolls, num, die):
   [newRolls,die] = roll(rolls.count(num),die)
   for value in newRolls:
      rolls.append(value)
   return rolls

def bigExplode(rolls, num, die, count):
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

def reroll(rolls, num, die, direction):
   for count in range(len(rolls)):
      if direction == "above":
         if rolls[count] > num:
            [[rolls[count]],temp] = roll(1, die)
            deeper = True
      if direction == "below":
         if rolls[count] < num:
            [[rolls[count]],temp] = roll(1, die)
            deeper = True
      if direction == "same":
         if rolls[count] == num:
            [[rolls[count]],temp] = roll(1, die)
   return rolls

def rerollInf(rolls, num, die, direction):
   deeper = False
   for count in range(len(rolls)):
      if direction == "above":
         if rolls[count] > num:
            [[rolls[count]],temp] = roll(1, die)
            deeper = True
      if direction == "below":
         if rolls[count] < num:
            [[rolls[count]],temp] = roll(1, die)
            deeper = True
      if direction == "same":
         if rolls[count] == num:
            [[rolls[count]],temp] = roll(1, die)
            deeper = True
   if deeper:
      rolls = reroll(rolls, num, die, direction)
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