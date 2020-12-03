#!/usr/bin/python3
# My working for day 3 part 1
#
# PROBLEM: Given an input "map" of trees (#) and space (.), which repeats
#          to the right, navigate from top to bottom going right 3, down 1
#          counting how many trees one would encounter on the way
import sys

#Load the "course" as a tree/blank array
slope = []
with open("day3_input.txt","r") as file:
    temp = file.read().splitlines() # Read whole file, chomp newlines
    for l in temp:
        line = list(l)
        slope.append(line)

#our current position on the course:
x = 0
y = 0

#the "finish line" is after we run off the end of the course
maxY = len(slope)

#Tessalation is horizontal so the "clock factor" is the length of the inner
#array
modX = len(slope[0])

#the per-move steps
deltaX = 3
deltaY = 1

print("Running for {0} lines (modulo {1} on x-axis)".format(maxY,modX))

numTrees = 0
while y < maxY:
    if slope[y][x] == '#':
        numTrees = numTrees + 1
    print("x={0},y={1} count={2}, last= {3}".format(x,y,numTrees,slope[y][x]))
    x = (x + deltaX) % modX
    y = y + deltaY

print("Arrived at finish! Hit {0} trees on the way!".format(numTrees))
