#!/usr/bin/python3
#
# My working for Day 15 Part 1
#
# PROBLEM:
#    The "Elf Game" has the following rules:
#       * There is a starting set of numbers
#       * At each turn AFTER the initial set of numbers
#         has been spoken, the player must either state
#         0 - the previous number has never been seen before
#         n - The previous number came up n turns ago.
#         (strictly speaking the difference between the last 2
#          utterences.)
#
#  Given an input starting set, determine the 2020th number spoken.

#Test Data. Answer = 1
startNumbers = [ 1,3,2 ]
#Test Data. Answer = 436
startNumbers = [ 0,3,6 ]
#Test, a= 10
startNumbers = [ 2,1,3 ]
#Test, a=27
startNumbers = [1,2,3]

#Actual puzzle input:
startNumbers = [ 0,5,4,1,10,14,7 ]

#How long should we play for?
targetTurn = 2020

#Here is a Glob to hold our number data.
nData = {}

###################################################################
#Setup the game:
def init_nData(refNumbers) :
    global nData
    i=1
    while i <= len(refNumbers) :
        print(f"Turn {i:4}, adding start number {refNumbers[i-1]}")
        nData[refNumbers[i-1]]=[i]
        i +=1
    return i
###################################################################
###################################################################
###################################################################
if __name__ == '__main__':
    i = init_nData(startNumbers)
    pNum = startNumbers[len(startNumbers)-1]
    while i <= targetTurn :
        #RULES:
        #  IF pNum was FIRST SPOKEN last turn, ANS=0
        #  ELSE: ANS = diff(last turn, last spoken)
        print(f"{i:5}:{pNum:5}",end=":")
        nextNumber = 0
        if pNum not in nData :
            #Satifies criteria "never previously spoken"
            print("(never)",end="")
        elif len(nData[pNum]) == 1:
            #Number has only been spoken once before.
            print("(once)",end="")
            if nData[pNum][0] == i-1 :
                #...And it was on the last turn.
                print("(last turn)",end="")
                nextNumber = 0
            else :
                #...but it was on a previous turn
                nextNumber = (i-1) - nData[pNum][0]
                print(f"(prev;{nData[pNum][0]})",end="")
        else :
            #Number has definitely been spoken before.
            l=len(nData[pNum])
            last=nData[pNum][l-1]
            prev=nData[pNum][l-2]
            nextNumber = last - prev
            print(f"(l:{last},p:{prev})",end="")
        print(f" SPEAK={nextNumber}")
        pNum=nextNumber
        #Update stats
        if nextNumber not in nData :
            nData[nextNumber] = [i]
        else :
            nData[nextNumber].append(i)
        i += 1

    print(f"Finishing turn {i-1}, last number spoken was {nextNumber}")
