#!/usr/bin/python3
# My working for day 3 part 2
#
# PROBLEM: Given an input "map" of trees (#) and space (.), which repeats
#          to the right, navigate from top to bottom following a set of
#          different defined slopes. Calculate the PRODUCT of the number of
#          trees encountered for each different slope.
#          slopes:   [dX=1,dY=1],[dX=3,dY=1],[dX=5,dY=1],[dX=7,dY=1],[dX=1,dY=2]
import sys

#Slopes is a definition too
slopes = [
    [1,1],
    [3,1],
    [5,1],
    [7,1],
    [1,2]
]

#Load the "course" as a tree/blank array
course = []
with open("day3_input.txt","r") as file:
    temp = file.read().splitlines() # Read whole file, chomp newlines
    for l in temp:
        line = list(l)
        course.append(line)

################################################################################
#We run the course a number of times so this becomes a function
def runSlopeAnalysis(course,deltaX,deltaY) :
    #our initial position on the course:
    x = 0
    y = 0
    #the "finish line" is after we run off the end of the course
    maxY = len(course)
    #Tessalation is horizontal so the "clock factor" is the length of the inner
    #array
    modX = len(course[0])

    numTrees = 0
    while y < maxY:
        if course[y][x] == '#':
            numTrees = numTrees + 1
        #print("x={0},y={1} count={2}, last= {3}".format(x,y,numTrees,slope[y][x]))
        x = (x + deltaX) % modX
        y = y + deltaY

    return(numTrees)
################################################################################

if __name__ == "__main__":

    treesEncountered = []
    run = 1
    treeProduct = 1
    for s in slopes:
        treesHit = runSlopeAnalysis(course,s[0],s[1])
        print("Run {0} (dX={1},dY={2}) hit {3} trees".format(run,s[0],s[1],treesHit))
        treeProduct = treeProduct * treesHit
        run = run + 1

    print("TreeProduct (answer) = {0}".format(treeProduct))
