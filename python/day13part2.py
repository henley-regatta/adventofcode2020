#!/usr/bin/python3
#
#   My solution for Day 13 Part 2
#
#   PROBLEM
#     Given an input list of :
#         <earliestDepartureEstimate>
#         [<BusID>|X],[<BusID|X]....
#
#     Where BusID = a number showing minutes-past-the-hour the bus departs
#        OR: X = Bus not in service.
#
#   IGNORE <earliestDepartureEstimate>.
#   What is the first DepartureTime at which each BusID departs sequentially
#   at i minutes past that DepartureTime?
#
#  (X gives a "free pass" for that minute-past-DepartureTime.)
#
import sys

#######################################################################################
def readBusList(datafile) :
    busList=[]
    with open(datafile,"r") as df:
        leaveEstimate=int(df.readline())
        o=0
        for x in df.readline().strip().split(","):
            try:
                busList.append([o,int(x)])
            except ValueError :
                pass
            o=o+1
    print(f" Offset/BusIDs: {busList}")
    return busList

#######################################################################################
#Something Something Chinese Remainder Theorem by Sieve method.
def GoogledAnswerStillDontUnderstand(busList,limit) :
    departureTime = 0
    increment = busList[0][1]
    print(f"For b= 0, dI={increment:2} : d={departureTime:15}, i={increment:15}")
    for offset, time in busList[1:] :
        oInc=0
        while (departureTime + offset) % time != 0 :
            departureTime += increment
            print(f"\t(o={oInc:3}, d={departureTime:15})")
            oInc += 1
        increment *= time
        print(f"For b={offset:2}, d={departureTime:15}, i={increment:15}")
    return departureTime


#######################################################################################
# This is the simple way of doing it, by iteration. The only optimisation I've made
# is to spot that we can "jump ahead" by the zeroth'd index busId number
# (this is still horrendously inefficient)
def simplisticAlgorithm(busList,limit) :
    #There's a simplistic algorithm where you just count up checking as you go....

    foundSequence=False
    departureTime=0
    bestSequenceLengthFound=0
    while not foundSequence and departureTime < limit :
        isCandStartTime = True
        nextBusDepartures = []
        for b in busList :
            #Still on-track if <departureTime>+offset is a start-time for bus
            if (departureTime+b[0]) % b[1] != 0 :
                isCandStartTime = False
                break
            else :
                nextBusDepartures.append([departureTime+b[0],b[1]])
        if isCandStartTime :
            print(f"\n\nFound Start Time {departureTime:,} because: {nextBusDepartures}")
            foundSequence=True
        else :
            #Making this a little easier, we only have to look at startTimes at which
            #the first bus in the list departs....
            if len(nextBusDepartures) > bestSequenceLengthFound :
                bestSequenceLengthFound = len(nextBusDepartures)
                print(f"\n(Partial solution (first {bestSequenceLengthFound}) at {departureTime} for {nextBusDepartures})")

            departureTime = departureTime + busList[0][1]
            if departureTime % (busList[0][1]*1000000) == 0 :
                print(f"{departureTime:,}",end='..',flush=True)

    if foundSequence :
        return departureTime
    else :
        print("Solution Not Found before Limit exceeded")
        exit(1)
        return -1


#######################################################################################
#Approaches based on common denominators are wrong, because the LCF is frequently
#bigger than the actual answer. And takes too long to compute anyway.
def maxAnswerSize(busList) :
    n = 1
    for b in busList :
        n = n * b[1]
    return n

#######################################################################################
#######################################################################################
#######################################################################################
if __name__ == "__main__":

    for df in [
        "../data/day13_test4.txt",
        "../data/day13_test3.txt",
        "../data/day13_test2.txt",
        "../data/day13_test1.txt",
        "../data/day13_input.txt"
        ] :
        print("="*80)
        busList=readBusList(df)
        limSize = maxAnswerSize(busList)
        print(f">>>>>>>>Solution must be less than {limSize:,}")
        answer1=GoogledAnswerStillDontUnderstand(busList,limSize)
        print(f"The Something Something Chinese Remainder Theorem by Sieving Answer is {answer1} ({answer1:,})")
        #answer2=simplisticAlgorithm(busList,limSize)
        print("-"*80)
        pctMax = (answer1 / limSize) * 100
        print(f">>>>>>>Answer is {pctMax:.1f}% of limit")
