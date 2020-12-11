#!/usr/bin/python3
#
# My solution for Day 11 Part 2
#
# PROBLEM:
#     You are given an input "Seat Map for a ferry"
#     (.=floor, L=seat, #=occupied seat). New arrivals will change seat state
#     according to rules similar to (BUT DIFFERENT FROM) Conway's Life
#       * Seat will be OCCUPIED (L->#) IF no "visible" seats are occupied.
#         (up,down,left,right and diagonals - 8 places)
#       * Seat will be VACATED (#->L) IF 5 or more "visible" seats are OCCUPIED
#       * No other seat will be modified.
#
# The "Visibility" rule applies thus:
#   From your position, iterate away in the given direction ignoring floor.
#   The state of the first seat encountered - not floor - determines the occupancy.
#
#  Iterate over a given input seat map applying the rules above until a steady-state
#  is arrived at. How many seats are occupied?
import sys
import copy

seatmapfile = "../data/day11_input.txt"
#seatmapfile = "../data/day11_test1.txt"

#You know things are going badly when...
debug=False

#This is a help throughout.....
t2i = {
    "." : 0,     # FLOOR
    "L" : -1,    # EMPTY SEAT
    "#" : 1      # OCCUPIED SEAT
}
i2t = {}
for c in t2i.keys() :
    i2t[t2i[c]] = c

#We need these numbers to guide our evaluation across the seatmap but we also
#can't set them until we've read the seatmap in...
maxR = 0 #Should be len(seatmap)-1
maxC = 0 #Should be len(seatmap[x])-1

###############################################################################
#Input is a tri-state bitmap.
def read_seatmap_from_file(filename) :
    seatmap=[]
    with open(filename,"r") as smf:
        for r in smf:
            r = r.strip()
            if len(r)>0 :
                row=[]
                for c in r:
                    row.append(t2i[c])
                seatmap.append(row)

    #Reset the globals for max dimensions
    global maxR
    maxR=len(seatmap)-1
    global maxC
    maxC=len(seatmap[1])-1 #Spot the implicit assumption: All rows are the same width.

    return seatmap

###############################################################################
#Vanity function - Pretty-print the seatmap like the input
def pretty_print_seatmap(seatmap) :
    for r in range(len(seatmap)) :
        for c in range(len(seatmap[r])) :
            print(i2t[seatmap[r][c]],end='')
        print()

###############################################################################
#Helper function. Calculate the "state" of the seating by assigning a number
#to each seatID based on occupation. Used later to calculate whether we've
#terminated or not.
# NOTE: The challenge conditions tell us "Iterate until number of seats remains
#       static". Strictly this isn't "steady-state" (gliders, iterators etc)
#       so this function is just a handy cheat instead of a proper state hash.
def calculate_state_number(seatmap) :
    stateNumber=0
    for r in range(len(seatmap)) :
        for c in range(len(seatmap[r])) :
            if seatmap[r][c] == 1 :
                stateNumber = stateNumber + 1
    return stateNumber

###############################################################################
#This is a helper to look away in a given direction from the start point
def firstChairState(orgr,orgc,dr,dc) :
    r=orgr #Initial position set
    c=orgc
    retV=t2i['.'] # Default return value = nothing.
    foundChair=False
    #There's always a special case. In this one, if dr and dc are both zero
    #there's no look-away; we're examining ourselves. Return blank.
    if dr==0 and dc==0 :
        foundChair=True
    #That's that dealt with, on to the more interesting cases:
    while not foundChair:
        c=c+dc #Increase look distance
        r=r+dr #Increase look distance
        if debug : print(f"?[{r},{c}]",end='')
        #Limit conditions
        if c<0 : foundChair=True
        elif c>maxC : foundChair=True
        elif r<0 : foundChair=True
        elif r>maxR : foundChair=True
        elif seatmap[r][c] != t2i['.'] :
            retV=seatmap[r][c]
            foundChair=True
    if debug: print(f"->({r},{c})={retV}",end='.')
    return retV

###############################################################################
#The main Rules of Life iterator function. Could possibly be split into
#per-row/per-col sub functions but hey ho
def iterate_seatmap_state(seatmap) :
    outputseatmap=copy.deepcopy(seatmap) #simple way of getting output map with same dimensions as input
    for r in range(len(seatmap)) :
        for c in range(len(seatmap[r])) :
            if debug: print(f"({r},{c}):", end='')
            #Default position is no change
            outputseatmap[r][c]=seatmap[r][c]
            #Skip floor elements by ignoring zeros
            if seatmap[r][c] != 0 :
                #The visibility rule has changed so the way we iterate over
                #neighbours must change. For each of the 8 directions we continue
                #looking "away" from the seat until reaching another seat OR the
                #boundary.
                adjacency=0
                for dr in [-1,0,+1] :
                    for dc in [-1,0,+1] :
                        if firstChairState(r,c,dr,dc) == t2i['#'] :
                            adjacency=adjacency+1
                if debug: print(f" sum={adjacency}", end='')
                #OK that's that calculated. How to iterate position?
                if adjacency>4 :
                    #5 or more nearby seats occupied => De-occupy the seat
                    outputseatmap[r][c]=t2i['L']
                if adjacency==0 :
                    #NO SEATS Occupied within adjacenct => Occupy the seat
                    outputseatmap[r][c]=t2i['#']
                #Falling off here means "no change" which is what we want...
            if debug: print(f" old:{i2t[seatmap[r][c]]}, new:{i2t[outputseatmap[r][c]]}")
    return outputseatmap

###############################################################################
###############################################################################
###############################################################################
if __name__ == "__main__":
    seatmap=read_seatmap_from_file(seatmapfile)
    #print(seatmap)
    oldState_Number=calculate_state_number(seatmap)
    #print(f"Initial State Number {oldState_Number}")
    pretty_print_seatmap(seatmap)
    haveReachedStasis=False
    iterations = 0
    while not haveReachedStasis :
        seatmap=iterate_seatmap_state(seatmap)
        iterations = iterations + 1
        newState_Number = calculate_state_number(seatmap)
        print("-"*30,end='')
        print(f"{iterations}: {oldState_Number}->{newState_Number}",end='')
        print("-"*30)
        pretty_print_seatmap(seatmap)
        if newState_Number == oldState_Number :
            haveReachedStasis=True
        oldState_Number = newState_Number

    print(f"Reached Seat Stasis after {iterations} iterations. Total occupied seats = {oldState_Number}")
