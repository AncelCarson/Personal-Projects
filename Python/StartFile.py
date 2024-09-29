# pylint: disable=invalid-name,bad-indentation,non-ascii-name
# -*- coding: utf-8 -*-

### Ancel Carson
### Created: 3/8/2020
### Updated: 28/9/2024
### Windows 11
### Python command line, VSCode
### StartFile.py

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


# Object Class
class Start():
    """Class Docstring.
    
    Functions:
        hello: prints "Hello"
        world: prints "World"
    """
    def hello(self):
        """Function Docstring.

        Parameters:
            self (self): Ths instance of this class 

        Returns:
            None (none_type): This is an example
        """
        print("Hello")

    def world(self):
        """Function Docstring."""
        print("World")

# Main Function
def main():
    """Function Docstring."""
    funct = Start()
    funct.hello()
    funct.world()

# Self Program Call
if __name__ == '__main__':
    main()
