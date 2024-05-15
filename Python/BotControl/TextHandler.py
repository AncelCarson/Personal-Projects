### Ancel Carson
### Created: 8/1/2020
### UPdated: 8/1/2023
### Windows 11
### Python command line, Notepad, IDLE
### TextHandler.py

# Libraries
import os
from time import sleep
from Roller import roller
from MenuMaker import menu
from threading import Thread
from datetime import datetime
from MenuMaker import makeMenu

# Object Class
class TextHandler:
    def __init__(self, id=None, title="...you", interface="cmd"):
        self.id = id
        self.title = title
        self.interface = interface
        self.answers = []
        self.mode = "waiting"
        self.channel = None

    def messageIn(self, message):
        text=[]

        if self.mode != "waiting":
            if self.mode == "thinking":
                text = [["One monent {0}. I am processing the last request".format(self.title),0]]
                return text
            else: 
                return text

        greeting = day_greeting()

        content = message.split(' ')
        try:
            if content[0] == "/Jeeves":
                text = [["Good {1} {0}. {2}".format(self.title, greeting[0], greeting[1]),0]]

            if content[0] == "/DM":
                self.mode = "userSetTest"
                text = [[f'Good {greeting[0]} {content[1]}. I am here to assist you',0],
                        ["Would you please tell me your First and Last Name?",1],
                        ["Are you Male (M) or Female (F)?",0],
                        ["Please answer with a single Character",1]]

            if content[0] == "/Response":
                self.mode = "responseTest"
                text = [['This is a call and response test',0],
                        ["What is response 1?",1],
                        ["Response 2?",1],
                        ["Pause for effect",0],
                        ["Response 3?",1]]

            if content[0] == "/roll":
                text = [[roller(content[1:]),0]]
                # for line in result:
                #     text.append([str(line),0])


        except Exception as e:
            text = [["Something has gone wrong. Please ask again",0]]
        
        return text

    def responseIn(self, answers):
        self.answers = answers
        self._thread = Thread(target=self.responseProcess, daemon=True)
        self._thread.start()
    
    def responseProcess(self):
        process = self.mode
        self.mode = "thinking"

        if process == "responseTest":
            print(self.answers)
            for i in range(10):
                print(i)
                sleep(1)
        self.mode = "waiting"

        if process == "userSetTest":
            print(self.answers)
            for i in range(10):
                print(i)
                sleep(1)

        sender(self, "Task Complete")
        self.mode = "waiting"

# Main Function
def main():
    textHandler = TextHandler()
    while True:
        answers = []
        text = textHandler.messageIn(input())
        for line in text:
            if line[1] == 0:
                print(line[0])
            elif line[1] == 1:
                answers.append(input(line[0]))
        if len(answers) > 0:
            endMsg = textHandler.responseIn(answers)
            print(endMsg)

def day_greeting():
    hour = datetime.now().hour
    if hour < 4: 
        time = "morning"
        greeting = "Up late are we?"
    elif hour < 6: 
        time = "morning"
        greeting = "Up early are we?"
    elif hour < 12: 
        time = "morning"
        greeting = "I am listening."
    elif hour < 16: 
        time = "afternoon"
        greeting = "I am listening."
    elif hour < 23: 
        time = "evening"
        greeting = "I am listening."
    else:
        time = "evening"
        greeting = "Will this be another long night?"

    return [time, greeting]

def sender(self, message):
    if self.interface == "cmd":
        print(message)
    if self.interface == "Discord":
        self.channel.send(message)

# Self Program Call
if __name__ == '__main__':
    main()