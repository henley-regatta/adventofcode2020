#!/usr/bin/python3
#
# My working for Day 15 Part 2
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
#  Given an input starting set, determine the 30000000th  number spoken.
#
# DISCUSSION: This is a trivial extension of the first part. So we'll just
#             time the answers to get an idea of how long it'll take to
#             do it, but I suspect the answer is BRUTE FORCE.
import time

#How long should we play for?
bigTarget = 30000000


#Test Data. Answer = 1
startNumbers = [ 1,3,2 ]

#Test, a= 10
startNumbers = [ 2,1,3 ]
#Test, a=27
startNumbers = [1,2,3]

#Test Data i=2020,a=438. i=30000000,a=18
startNumbers = [3,2,1]

#Test Data i=2020, a=436. i=30000000, a=175594
startNumbers = [ 0,3,6 ]

#Actual puzzle input:
startNumbers = [ 0,5,4,1,10,14,7 ]

#Here is a Glob to hold our number data.
nData = {}

###################################################################
#Setup the game:
def init_nData(refNumbers) :
    global nData
    i=1
    while i <= len(refNumbers) :
        nData[refNumbers[i-1]]={ 'l' : i, 'p' : 0 }
        i +=1
    return i
###################################################################
#Play the game:
def play_game(initNumbers,targetTurn) :
    global nData
    i = init_nData(startNumbers)
    pNum = startNumbers[len(startNumbers)-1]
    tStart = time.time()
    while i <= targetTurn :
        #RULES:
        #  IF pNum was FIRST SPOKEN last turn, ANS=0
        #  ELSE: ANS = diff(last turn, last spoken)
        nextNumber = 0
        if pNum not in nData :
            #Satifies criteria "never previously spoken"
            pass
        elif nData[pNum]['p'] == 0 :
            #Number has only been spoken once before.
            if nData[pNum]['l'] <= i-1 :
                #...but it was on a previous turn
                nextNumber = (i-1) - nData[pNum]['l']
        else :
            #Number has definitely been spoken before.
            nextNumber = nData[pNum]['l'] - nData[pNum]['p']
        pNum=nextNumber
        if nextNumber not in nData :
            nData[nextNumber] = {'l' : i, 'p' : 0 }
        else :
            newPrev = nData[nextNumber]['l']
            nData[nextNumber] = { 'l' : i, 'p' : newPrev}
        i += 1

    print(f"Finishing turn {i-1}, last number spoken was {nextNumber}")
    tEnd = time.time()
    tDiff = tEnd - tStart
    tRate = targetTurn / tDiff
    print(f"(elapsed time: {tDiff:3.3f}, turns/sec: {tRate:1.2f})")
    return nextNumber, tRate

###################################################################
###################################################################
if __name__ == '__main__':
    print(startNumbers)
    ans,rate = play_game(startNumbers,2020)
    estTimeToBigTarget = bigTarget / rate
    print(f"Estimated time to finish {bigTarget} rounds: {estTimeToBigTarget:1.2f} Seconds")
    print("-"*80)
    nData={} #See if you can spot the last code edit to solve the "IT'S NOT WORKING ON BIG ITERATIONS!" arrghg...
    ans,rate = play_game(startNumbers,bigTarget)
