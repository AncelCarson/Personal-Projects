### Ancel Carson
### 7/24/2019
### Windows 10
### Python command line, Notepad, IDLE

# Object Class
disks =['                 ',
        '        1        ',
        '       222       ',
        '      33333      ',
        '     4444444     ',
        '    555555555    ',
        '   66666666666   ',
        '  7777777777777  ',
        ' 888888888888888 ',
        '99999999999999999']

stackA=[]
stackB=[]
stackC=[]

# Main Function
def main():
    diskNum = int(input('How many disks do you want? (1-9)\n'))
    for num in range(diskNum):
        stackA.append(disks[num+1])
    printTowers()
    moveIt(diskNum, stackA, stackB, stackC)
    input('End program')
    
def moveIt(n, from_rod, to_rod, aux_rod):
    if n > 0:
        moveIt(n - 1, from_rod, aux_rod, to_rod)
        to_rod.insert(0,from_rod.pop(0))
        printTowers()
        moveIt(n - 1, aux_rod, to_rod, from_rod)

def printTowers():
    tallest = max(len(stackA),len(stackB),len(stackC))
    for row in reversed(range(tallest)):
        if row <= len(stackA)-1:
            aDisk = stackA[len(stackA)-(row+1)]
        else:
            aDisk = disks[0]
        if row <= len(stackB)-1:
            bDisk = stackB[len(stackB)-(row+1)]
        else:
            bDisk = disks[0]
        if row <= len(stackC)-1:
            cDisk = stackC[len(stackC)-(row+1)]
        else:
            cDisk = disks[0]
        print(aDisk,bDisk,cDisk,)
    print('------------------------------------------------------')

# Self Program Call
if __name__ == '__main__':
    main()
