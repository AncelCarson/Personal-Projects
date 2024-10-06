# pylint: disable=invalid-name,bad-indentation,non-ascii-name,unnecessary-lambda-assignment
# -*- coding: utf-8 -*-

# Author: Ancel Carson
# Orginization: Napps Technology Comporation
# Creation Date: 20/6/2022
# Update Date: 20/6/2022
# MenuMaker.py
# Rev 1

"""Variable Size Menu Creater.

Program receives a list of items consisting of a title and options. It will 
then create items that are sized to havwe a uniform menu.

Functions:
   menu: Driver of the program
   makeMenu: Function called by other programs
   maxLength: Finds the max length of the list
"""

# Main Function
def menu(MenuItems):
   """Takes a list of items and displays them as a selectable menu."""
   title = MenuItems[0]
   length = maxLength(MenuItems)
   if len(title) == length:
      title = " " + title
      length = length + 1

   diff = length - len(title) + 1
   cSpace = " " * int(diff / int(2))
   title = cSpace + title + cSpace
   if diff%2 != 0:
      title = title + " "

   spacer = "-" * (length + 1)
   MenuItems[0] = spacer
   MenuItems.append(spacer)
   wrapping = lambda item: "|" + item + "|"
   print("\n" + wrapping(title))
   for item in MenuItems:
      option = item + (" " * (length - len(item) + 1))
      print(wrapping(option))

def makeMenu(title, lst):
   """Takes a title and list of options anf formats them for the menu function."""
   menuList = [title]
   count = 0
   for item in lst:
      count += 1
      menuList.append(str(str(count) + ": " + item))
   menu(menuList)

def maxLength(lst):
   """Returns the length of the largest item in the list"""
   maxLengthValue = max(len(x) for x in lst)
   return maxLengthValue


# Self Program Call
if __name__ == "__main__":
   menu(["Fruit","A: Apple","B: Orange","C: Pear","D: Grape","E: Pomegranite"])
