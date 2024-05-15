### Ancel Carson
### Created: 14/9/2023
### Updated: 14/9/2023
### Windows 11
### Python command line, Notepad, IDLE
### Heat Pump State machine.py

# Libraries

# Object Class
class Chiller():
   def __init__(self, number):
      self.number = number    # Unit Number in Array
      self.state = "Off"      # Current State of the Unit
      self.runtime = 0
      self.chilledLoad = 0    # Percentage of Total Cooling Capacity
      self.heatLoad = 0       # Percentage of Total Cooling Capacity
      self.heatMax = 100      # Percentage of Total Unit Heating Capacity Currently Available
      # Valve States
      self.valvesOpen = {"Chilled": False, "HR": False, "Hot": False}
   
   # Set Unit to Cooling Mode
   def startCool(self):
      self.state = "Cooling"
      self.setValves()
   
   # Set Unit to Heat Recovery Mode
   def startHR(self):
      self.state = "HeatRecovery"
      self.setValves()
   
   # Set Unit to Heating Mode
   def startHeat(self):
      self.state = "Heating"
      self.setValves()
   
   # Set Unit to Off Mode
   def turnOff(self):
      self.state = "Off"
      self.chilledLoad = 0
      self.heatLoad = 0
      self.setValves()

   def runTick(self):
      if self.state != "Off":
         self.runtime += 1
   
   # Returns the Current State of the Unit
   def getState(self):
      return self.state
   
   # Returns the number of Cycles a Unit has been running
   def getRuntime(self):
      self.runtime
   
   # Returns the Percetage of Unit Maximum Chilled Load Currently Running
   def getChilledLoad(self):
      return self.chilledLoad
   
   # Returns the Percetage of Unit Maximum Heating Load Currently Running
   def getHeatLoad(self):
      return self.heatLoad
   
   # Sets the Percetage of Unit Maximum Chilled Load Currently Running
   def setChilledLoad(self, value):
      self.chilledLoad = value
   
   # Sets the Percetage of Unit Maximum Heating Load Currently Running
   def setHeatLoad(self, value):
      self.heatLoad = value

   # Sets the valve states based off of the Current Unit State
   def setValves(self):
      if self.state == "Cooling":
         self.valvesOpen = {"Chilled": True, "HR": False, "Hot": False}
      if self.state == "HeatRecovery":
         self.valvesOpen = {"Chilled": True, "HR": True, "Hot": False}
      if self.state == "Heating":
         self.valvesOpen = {"Chilled": False, "HR": False, "Hot": True}
      if self.state == "Off":
         self.valvesOpen = {"Chilled": False, "HR": False, "Hot": False}

   # Displays in thest the current state of the Unit
   def showStatus(self):
      print("|  Unit #{} Current Operation  |".format(self.number))
      print("--------------------------------")
      print("Current State: {}".format(self.state))
      print("--------------------------------")
      print("Percent Cooling Capacity: {}%".format(self.chilledLoad))
      print("Percent Heating Capacity: {}%".format(self.heatLoad))
      print("--------------------------------")
      print("Chilled Valve Open: {}".format(self.valvesOpen["Chilled"]))
      print("HeatRec Valve Open: {}".format(self.valvesOpen["HR"]))
      print("Heating Valve Open: {}".format(self.valvesOpen["Hot"]))
      print("--------------------------------\n")

# Main Function
class Array():
   def __init__(self):
      self.arrayCoolingLoad = 0
      self.arrayHeatingLoad = 0
      self.setCooling = 0
      self.setHeating = 0

      self.unitCount = int(input("How many units are in the Array?\n"))   # Gets Number of Units Needed
      self.units = [Chiller(count + 1) for count in range(self.unitCount)]     # Creates and Array of Chillers
      self.arrayStatus = lambda: [unit.showStatus() for unit in self.units]    # Creates Array Display Variable
      self.arrayStatus()
      self.runArray()

   def runArray(self):
      self.running = True
      while (self.running):
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
      if self.loadChange[1] == "Decrease":
         if self.setCooling == 0:
            [unit.turnOff() for unit in self.units]
      if self.loadChange[1] == "Increase":
         if self.unitCount - self.arrayState[1] > 0:
            if self.loadChange[0] == "Cooling":
               pass


   def handleHeating(self):
      if self.loadChange[1] == "Decrease":
         if self.setHeating == 0:
            [unit.turnOff() for unit in self.units]
      if self.loadChange[1] == "Increase":
         if self.unitCount - self.arrayState[1] > 0:
            if self.loadChange[0] == "Heating":
               pass


   def handleHR(self):
      pass

   def handleMixed(self):
      pass

   def getArrayState(self):
      states = [unit.getState() for unit in self.units]
      running = len(self.units) - states.count("Off")
      uniqueStates = list(set(states))
      uniqueStates.remove('Off')
      if len(uniqueStates) == 0:
         return ["Off", len(self.units)]
      elif len(uniqueStates) == 1:
         return [uniqueStates, running]
      else:
         return ["Mixed", running]

   def checkLoad(self):
      oldCool = self.arrayCoolingLoad
      oldHot = self.arrayHeatingLoad
      newCool = self.setCooling
      newHot = self.setHeating
      if newCool > oldCool:
         return["Cool", "Increase"]
      elif newCool < oldCool:
         return["Cool", "Decrease"]
      elif newHot > oldHot:
         return["Hot", "Increase"]
      elif newHot < oldHot:
         return["Hot", "Decrease"]
      else:
         return 0

def menu():
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