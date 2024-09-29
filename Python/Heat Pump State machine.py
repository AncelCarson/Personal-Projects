# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 14/9/2023
### Updated: 14/9/2023
### Windows 11
### Python command line, Notepad, IDLE
### Heat Pump State machine.py

"""Supervisor Controller State Machine for HP/HR Chillers.

Given a set number of "units" this program will simulate the running
and mode change based on current simulated modes.

Classes:
   Chiller: Chiller object
   Array: Objects made up of chillers

Functions:
   menu: Asks the user what they want to do
"""

# Libraries

# Object Class
class Chiller():
   """Chiller object that maintains its individual state.

   Variables:
      number (int): Unit number in an Array
      state (str): Current State of the Machine
      runtime (int): Time the unit has been running
      chilledLoad (float): Percentage of Total Cooling Capacity
      heatLoad (float): Percentage of Total Heating Capacity
      heatMax (float): Percentage of Total Unit Heating Capacity Currently Available
      valvesOpen (List -> Bool): Current staate of Water Valves

   Functions:
      startCool: Starts the unit in Cooling Mode
      startHR: Starts the unit in Heat Recovery Mode
      startHeat: Starts the unit in Heat Pump Mode
      turnOff: Turns the unit off
      runTick: Advances the unit 1 "tick"
      getState: Gets the current mode
      getRuntime: Gets how long th unit has been running
      getChilledLoad: Gets the current Chilling Load
      getHeatLoad: Gets the current Heating Load
      setChilledLoad: Sets the desired Chilling Load
      setHeatLoad: Sets the desired Heating Load
      setValues: Sets the Valve States
      showStatus: Gives a collection of data at once
      """
   def __init__(self, number):
      self.number = number    # Unit Number in Array
      self.state = "Off"      # Current State of the Unit
      self.runtime = 0
      self.chilledLoad = 0    # Percentage of Total Cooling Capacity
      self.heatLoad = 0       # Percentage of Total Cooling Capacity
      self.heatMax = 100      # Percentage of Total Unit Heating Capacity Currently Available
      # Valve States
      self.valvesOpen = {"Chilled": False, "HR": False, "Hot": False}

   def startCool(self):
      """Puts the unit in Cooling Mode."""
      self.state = "Cooling"
      self.setValves()

   def startHR(self):
      """Puts the unit in Heat Recovery Mode."""
      self.state = "HeatRecovery"
      self.setValves()

   def startHeat(self):
      """Puts the unit in Heating Mode."""
      self.state = "Heating"
      self.setValves()

   def turnOff(self):
      """Turns the unit off."""
      self.state = "Off"
      self.chilledLoad = 0
      self.heatLoad = 0
      self.setValves()

   def runTick(self):
      """Increases runtime by one."""
      if self.state != "Off":
         self.runtime += 1

   def getState(self):
      "Returns the current state of the unit."
      return self.state

   def getRuntime(self):
      """Returns the number of Cycles a Unit has been running."""
      return self.runtime

   def getChilledLoad(self):
      """Returns the Percetage of Unit Maximum Chilled Load Currently Running."""
      return self.chilledLoad

   def getHeatLoad(self):
      """Returns the Percetage of Unit Maximum Heating Load Currently Running."""
      return self.heatLoad

   def setChilledLoad(self, value):
      """Sets the Percetage of Unit Maximum Chilled Load Currently Running."""
      self.chilledLoad = value

   def setHeatLoad(self, value):
      """Sets the Percetage of Unit Maximum Heating Load Currently Running."""
      self.heatLoad = value

   def setValves(self):
      """Sets the valve states based off of the Current Unit State."""
      if self.state == "Cooling":
         self.valvesOpen = {"Chilled": True, "HR": False, "Hot": False}
      if self.state == "HeatRecovery":
         self.valvesOpen = {"Chilled": True, "HR": True, "Hot": False}
      if self.state == "Heating":
         self.valvesOpen = {"Chilled": False, "HR": False, "Hot": True}
      if self.state == "Off":
         self.valvesOpen = {"Chilled": False, "HR": False, "Hot": False}

   def showStatus(self):
      """Displays the current state of the Unit."""
      print(f"|  Unit #{self.number} Current Operation  |")
      print("--------------------------------")
      print(f"Current State: {self.state}")
      print("--------------------------------")
      print(f"Percent Cooling Capacity: {self.chilledLoad}%")
      print(f"Percent Heating Capacity: {self.heatLoad}%")
      print("--------------------------------")
      print(f'Chilled Valve Open: {self.valvesOpen["Chilled"]}')
      print(f'HeatRec Valve Open: {self.valvesOpen["HR"]}')
      print(f'Heating Valve Open: {self.valvesOpen["Hot"]}')
      print("--------------------------------\n")

# Main Function
class Array():
   """Driver of the program and coordinator of the Units
   
   Variables:
      arrayCoolingLoad (float): Current Cooling load on the array
      arrayHeatingLoad (float): Current Heating load on the array
      setCooling (float): Set the desired Cooling Load
      setHeating (float): Set the desired Heating Load
      unitCount (int): The number of units in the array set by the user
      units (List -> Chillers): List of Chillers objects in the Array
      arrayStatus (lambda): Function that shows the current status of all Chillers
      running (bool): If the Array is running or not
      loadChange (list -> str): How the load is changing
      arrayState (str): The Current State of the Array

   Functions:
      runArray: Main function that holds the Run Loop
      handleCooling: Handles array adjustments when in Cooling Mode
      handleHeating: Handles array adjustments when in Heating Mode
      handleHR: Handles array adjustments when in Heat Recovery Mode
      handleMixed: Handles array adjustments when in Mixed Mode
      getArrayState: Gets the current state of the array
      checkLoad: Checks if the load has chenged since the last loop
   """
   def __init__(self):
      self.arrayCoolingLoad = 0
      self.arrayHeatingLoad = 0
      self.setCooling = 0
      self.setHeating = 0

      self.unitCount = int(input("How many units are in the Array?\n"))
      self.units = [Chiller(count + 1) for count in range(self.unitCount)]
      self.arrayStatus = lambda: [unit.showStatus() for unit in self.units]
      self.arrayStatus()
      self.runArray()

   def runArray(self):
      """Main function of the class that hold the running while loop"""
      self.running = True
      while self.running:
         self.loadChange = self.checkLoad()
         self.arrayState = self.getArrayState()
         if self.loadChange != 0:
            if self.arrayState[0] == "Cooling":
               self.handleCooling()
            if self.arrayState[0] == "Heating":
               self.handleHeating()
            if self.arrayState[0] == "HeatRecovery":
               self.handleHR()
            if self.arrayState[0] == "Mixed":
               self.handleMixed()

         self.running = False

   def handleCooling(self):
      """Handles Array Staging when all units are in Cooling Mode."""
      if self.loadChange[1] == "Decrease":
         if self.setCooling == 0:
            for unit in self.units:
               unit.turnOff()
      if self.loadChange[1] == "Increase":
         if self.unitCount - self.arrayState[1] > 0:
            if self.loadChange[0] == "Cooling":
               pass


   def handleHeating(self):
      """Handles Array Staging when all units are in Heating Mode."""
      if self.loadChange[1] == "Decrease":
         if self.setHeating == 0:
            for unit in self.units:
               unit.turnOff()
      if self.loadChange[1] == "Increase":
         if self.unitCount - self.arrayState[1] > 0:
            if self.loadChange[0] == "Heating":
               pass


   def handleHR(self):
      """Handles Array Staging when all units are in Heat Recovery Mode."""

   def handleMixed(self):
      """Handles Array Staging when multiple units are in different Modes."""

   def getArrayState(self):
      """Gets the current state of the array and how many units are running."""
      states = [unit.getState() for unit in self.units]
      running = len(self.units) - states.count("Off")
      uniqueStates = list(set(states))
      uniqueStates.remove('Off')
      if len(uniqueStates) == 0:
         return ["Off", len(self.units)]
      if len(uniqueStates) == 1:
         return [uniqueStates, running]
      return ["Mixed", running]

   def checkLoad(self):
      """Compares previous values to new values seeing if there is an adjustment."""
      oldCool = self.arrayCoolingLoad
      oldHot = self.arrayHeatingLoad
      newCool = self.setCooling
      newHot = self.setHeating
      if newCool > oldCool:
         return["Cool", "Increase"]
      if newCool < oldCool:
         return["Cool", "Decrease"]
      if newHot > oldHot:
         return["Hot", "Increase"]
      if newHot < oldHot:
         return["Hot", "Decrease"]
      return 0

def menu():
   """A list of operations for the user to choose."""
   print("| What would you like to do?  |")
   print("|-----------------------------|")
   print("| 1) Adjust Cooling Load      |")
   print("| 2) Adjust Heating Load      |")
   print("| 3) Check Array Status       |")
   print("| 4) Check All Unit Status    |")
   print("| 5) Check Single Unit Status |")
   print("| 6) End Simulation           |")
   print("|-----------------------------|")
   return int(input("Menu selection:\n"))

# Self Program Call
if __name__ == '__main__':
   array = Array()
