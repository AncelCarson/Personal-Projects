# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### 3/8/2020
### Windows 10
### Python command line, Notepad, IDLE

"""A simple FizzBuzz Program.

The program will print a string of numbers 1 after the other. Every 3rd number
it will print Fizz instead of the number. Every 5th number, it will print Buzz
instead of the number. When both happen at the same time, it will print FuzzBuzz.

Functions:
   main: Driver of the program
"""

# Main Function
def main():
    """Driver of the program"""
    count = 0
    maxVal = int(input("How high would you like to go?\n"))
    while count < maxVal:
        count = count + 1
        if count % 15 == 0:
            print("FizzBuzz")
        elif count % 5 == 0:
            print("Buzz")
        elif count % 3 == 0:
            print("Fizz")
        else:
            print(count)

# Self Program Call
if __name__ == '__main__':
    main()
