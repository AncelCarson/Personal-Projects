### Ancel Carson
### 3/8/2020
### Windows 10
### Python command line, Notepad, IDLE

# Main Function
def main():
    count = 0
    maxVal = int(input("How high would you like to go?\n"))
    while(count < maxVal):
        count = count + 1
        if(count % 15 == 0):
            print("FizzBuzz")
        elif(count % 5 == 0):
            print("Buzz")
        elif(count % 3 == 0):
            print("Fizz")
        else:
            print(count)
        

# Self Program Call
if __name__ == '__main__':
    main()