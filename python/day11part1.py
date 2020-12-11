#!/usr/bin/python3
#
# My solution for Day 11 Part 1
#
# PROBLEM:
#     You are given an input "Seat Map for a ferry"
#     (.=floor, L=seat, #=occupied seat). New arrivals will change seat state
#     according to rules similar to  Conway's Life
#       * Seat will be OCCUPIED (L->#) IF no adjacent seats are occupied.
#         (up,down,left,right and diagonals - 8 places)
#       * Seat will be VACATED (#->L) IF 4 or more adjacent seats are OCCUPIED
#       * No other seat will be modified.
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
#The main Rules of Life iterator function. Could possibly be split into
#per-row/per-col sub functions but hey ho
def iterate_seatmap_state(seatmap) :
    outputseatmap=copy.deepcopy(seatmap) #simple way of getting output map with same dimensions as input
    #Iterate over the range.
    maxR=len(seatmap)-1
    maxC=len(seatmap[0])-1 #Assumption throughout is that the number of columns is static.
    for r in range(len(seatmap)) :
        for c in range(len(seatmap[r])) :
            if debug: print(f"({r},{c}):", end='')
            #Default position is no change
            outputseatmap[r][c]=seatmap[r][c]
            #Skip floor elements by ignoring zeros
            if seatmap[r][c] != 0 :
                rRange=[]
                cRange=[]
                if r==0 : rRange=[0,1]
                elif r==maxR : rRange=[r-1,r]
                else : rRange = [r-1,r,r+1]
                if c==0 : cRange=[0,1]
                elif c==maxC : cRange=[c-1,c]
                else : cRange=[c-1,c,c+1]
                #Calculate "Adjacency" as sum of seats occupied around this one
                adjacency=0
                for cr in rRange :
                    for cc in cRange :
                        if debug: print(f"[({cr},{cc})={i2t[seatmap[cr][cc]]}]",end='')
                        if cc == c and cr == r :
                            continue # Don't count ourselves in adjacency
                        elif seatmap[cr][cc] == t2i["#"] :
                            adjacency=adjacency+1
                if debug: print(f" sum={adjacency}", end='')
                #OK that's that calculated. How to iterate position?
                if adjacency>3 :
                    #4 or more nearby seats occupied => De-occupy the seat
                    outputseatmap[r][c]=-1
                if adjacency==0 :
                    #NO SEATS Occupied within adjacenct => Occupy the seat
                    outputseatmap[r][c]=1
                #Falling off here means "no change" which is what we want...
            if debug: print(f" old:{seatmap[r][c]}, new:{outputseatmap[r][c]}")
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
