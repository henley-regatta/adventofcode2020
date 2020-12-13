#!/usr/bin/python3
#
#   My solution for Day 13 Part 1
#
#   PROBLEM
#     Given an input list of :
#         <earliestDepartureEstimate>
#         [<BusID>|X],[<BusID|X]....
#
#     Where BusID = a number showing minutes-past-the-hour the bus departs
#        OR: X = Bus not in service.
#
#   What is the ID of the first bus you can take after <earliestDepartureEstimate> ?
#   How many minutes will you have to wait for this bus?
#   Give the answer as <busID> * <minutesToWait>
#
import sys

datafile="../data/day13_input.txt"
#datafile="../data/day13_test1.txt"

leaveEstimate=0
busList=[]
with open(datafile,"r") as df:
    leaveEstimate=int(df.readline())
    for x in df.readline().strip().split(","):
        try:
            busList.append(int(x))
        except ValueError :
            pass

print(f"Leave Estimate: {leaveEstimate}, BusIDs: {busList}")

#Work out for each bus how close to the leaveEstimate this bus is coming:
nextBus = { 'waitTime' : 9999, 'id' : 0 }
for id in busList :
    timeToWait = (id * ((leaveEstimate // id)+1)) - leaveEstimate
    if timeToWait < nextBus['waitTime'] :
        nextBus = { 'waitTime' : timeToWait, 'id' : id }
    print(f"Bus {id:3} has a wait time of {timeToWait:3}")

AnswerWeSeek = nextBus['waitTime'] * nextBus['id']
print(f"Our next bus is: {nextBus} and the anwer we seek to part 1 is {AnswerWeSeek}")
