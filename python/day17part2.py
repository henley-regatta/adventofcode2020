#!/usr/bin/python3
#
# My solution for Day 17 Part 2
#
# PROBLEM:
#     Given an input "Start Condition" for a conway-like 4 dimensional grid,
#     work out the final state - the number of "active" cells - after 6
#     stages.
#      * All cells evaluate simultaneously
#      * Cell state depends on the state of all cells 1 cell away from the cell
#        (in 3 dimensions, i.e. there are up to 80 affecting cells)
#        NOTE: This is a "pocket dimension" so the boundaries wrap
#        (i.e. cells at one "edge" are adjacent to cells at the opposite "edge"
#      * An "Active" cell (#) stays active if 2 or 3 neighbours are active
#      * An "Active" cell becomes inactive (.) if <2 or >3 neighbours are active
#      * An "Inactive" cell becomes active if exactly 2 neighbours are active.
#
#   Note that the initial state loaded is a 2-dimensional grid; later iterations
#   will "grow" away from that at a rate of 1 cell per cycle.

import sys
import copy
from collections import defaultdict

initialstatefile = "../data/day17_input.txt"
#initialstatefile = "../data/day17_test1.txt"

#You know things are going badly when...
debug=False

#This is a help throughout.....
t2i = {
    "." : 0,     # inactive
    "#" : 1      # active
}
i2t = {}
for c in t2i.keys() :
    i2t[t2i[c]] = c

#THIS FEELS VERY WRONG
state = defaultdict(lambda :defaultdict(lambda :defaultdict(lambda : defaultdict(int))))
sDim = { 'w': [0,0], 'x': [0,0], 'y': [0,0], 'z': [0,0] }
###############################################################################
#Input is a bi-state input, arbitrarily at z=1
# Coordinates implicitly in x,y,z format
def read_state_from_file(filename) :
    global state
    global sDim
    with open(filename,"r") as smf:
        yCount = 0
        for r in smf:
            r = r.strip()
            if len(r)>0 :
                xCount = 0
                for c in r:
                    state[0][xCount][yCount][0] = t2i[c]
                    xCount += 1
                sDim['x'][1] = xCount-1
            yCount += 1
    sDim['y'][1] = yCount-1
    sDim['z'] = [ 0, 0]
    sDim['w'] = [ 0, 0]


###############################################################################
#Vanity function - Pretty-print the seatmap like the input
def pretty_print_state() :
    global state
    global sDim
    w=sDim['w'][0]
    while w<=sDim['w'][1] :
        print("+"*10, f" w= {w}", "+"*10)
        z=sDim['z'][0]
        while z <= sDim['z'][1] :
            print("-"*10, f" z= {z}", "-"*10)
            y=sDim['y'][0]
            while y <= sDim['y'][1] :
                x=sDim['x'][0]
                while x <= sDim['x'][1] :
                    print(i2t[state[w][x][y][z]],end='')
                    x += 1
                print()
                y += 1
            print()
            z += 1
        w+=1

###############################################################################
#Helper function. Calculate the "state" of the dimension by summing the active
#cells throughout
def calculate_state_number() :
    stateNumber=0
    global state
    global sDim
    w=sDim['w'][0]
    while w <= sDim['w'][1] :
        z=sDim['z'][0]
        while z <= sDim['z'][1] :
            y=sDim['y'][0]
            while y <= sDim['y'][1] :
                x=sDim['x'][0]
                while x <= sDim['x'][1] :
                    stateNumber += state[w][x][y][z]
                    x += 1
                y += 1
            z += 1
        w += 1
    return stateNumber

###############################################################################
# At the start of every iteration, grow the dimension by 1 cell in each direction
# (virtually....)
def grow_dimension() :
    global state
    global sDim
    sDim['z'] = [ sDim['z'][0]-1, sDim['z'][1]+1]
    sDim['y'] = [ sDim['y'][0]-1, sDim['y'][1]+1]
    sDim['x'] = [ sDim['x'][0]-1, sDim['x'][1]+1]
    sDim['w'] = [ sDim['w'][0]-1, sDim['w'][1]+1]

    #Initialise the new values to zero: Z-plane
    for z in sDim['z'] :
        w = sDim['w'][0]
        while w <= sDim['w'][1] :
            y = sDim['y'][0]
            while y <= sDim['y'][1] :
                x = sDim['x'][0]
                while x <= sDim['x'][1] :
                    state[w][x][y][z] = 0
                    x+=1
                y+=1
            w+=1
    #Initialise new values to zero on the Y-plane
    for y in sDim['y'] :
        w = sDim['w'][0]
        while w <= sDim['w'][1] :
            z = sDim['z'][0]
            while z <= sDim['z'][1] :
                x = sDim['x'][0]
                while x <= sDim['x'][1] :
                    state[w][x][y][z] = 0
                    x +=1
                z+=1
            w += 1

    #initialise the X-plane to zero:
    for x in sDim['x'] :
        w = sDim['w'][0]
        while w <= sDim['w'][1] :
            z = sDim['z'][0]
            while z <= sDim['z'][1] :
                y = sDim['y'][0]
                while y <= sDim['y'][1] :
                    state[w][x][y][z] = 0
                    y +=1
                z+=1
            w += 1
    #Initialise the new values to zero on the W-plane:
    for w in sDim['w'] :
        z = sDim['z'][0]
        while z <= sDim['z'][1] :
            y = sDim['y'][0]
            while y <= sDim['y'][1] :
                x = sDim['x'][0]
                while x <= sDim['x'][1] :
                    state[w][x][y][z] = 0
                    x+=1
                y+=1
            z+=1

###############################################################################
# HERE'S THE FUN BIT. Working out the neighbour state for a given cell
def calcActiveNeighbours(w,x,y,z) :
    global state
    global sDim

    #Work out the cells to check based on boundary conditions
    wCheck = [w-1,w,w+1]
    xCheck = [x-1,x,x+1]
    yCheck = [y-1,y,y+1]
    zCheck = [z-1,z,z+1]

    if w==sDim['w'][0] :
        wCheck[0]=sDim['w'][1]
    elif w==sDim['w'][1] :
        wCheck[1]=sDim['w'][0]

    if x==sDim['x'][0] :
        xCheck[0]=sDim['x'][1] #Wrap-around to max
    elif x==sDim['x'][1] :
        xCheck[2]=sDim['x'][0] #Wrap-around to min

    if y==sDim['y'][0] :
        yCheck[0]=sDim['y'][1]
    elif y==sDim['y'][1] :
        yCheck[2]=sDim['y'][0]

    if z==sDim['z'][0] :
        zCheck[0]=sDim['z'][1]
    elif z==sDim['z'][1] :
        zCheck[2]=sDim['z'][0]

    #OK, time to iterate....
    aCount = 0
    for cz in zCheck :
        for cy in yCheck :
            for cx in xCheck :
                for cw in wCheck :
                    #SKIP OURSELF
                    if cz==z and cy==y and cx==x and cw==w :
                        pass
                    else :
                        aCount += state[cw][cx][cy][cz]
    return aCount

###############################################################################
# Principle function for iterating - calculate the new state for each point on the
# "new" grid.
def determine_new_state() :
    global state
    global sDim
    newState = copy.deepcopy(state)
    #At it's core, this is dead easy....
    z=sDim['z'][0]
    while z <= sDim['z'][1] :
        y=sDim['y'][0]
        while y <= sDim['y'][1] :
            x=sDim['x'][0]
            while x<= sDim['x'][1] :
                w=sDim['w'][0]
                while w<= sDim['w'][1] :
                    activeNeighbours=calcActiveNeighbours(w,x,y,z)
                    if debug : print(f"({w},{x},{y}{z}) oldState={state[w][x][y][z]} Neighbours={activeNeighbours} ",end="")
                    if state[w][x][y][z] == 0 and activeNeighbours == 3 :
                        newState[w][x][y][z] = 1
                    elif activeNeighbours < 2 or activeNeighbours > 3 :
                        newState[w][x][y][z] = 0
                    else :
                        pass #State remains the same
                    if debug : print(f"newState={newState[w][x][y][z]}")
                    w+=1
                x+=1
            y+=1
        z+=1

    state=copy.deepcopy(newState)

###############################################################################
###############################################################################
###############################################################################
if __name__ == "__main__":
    read_state_from_file(initialstatefile)
    pretty_print_state()
    stateCount=calculate_state_number()
    iterations=0
    print(f"Initial State Count (i={iterations}): {stateCount}")
    while iterations <6 :
        iterations += 1
        print("="*20, f" ITERATION : {iterations} ", "="*20)
        #Grow the space available by 1
        grow_dimension()
        pretty_print_state()
        determine_new_state()
        stateCount=calculate_state_number()
        pretty_print_state()
        print(f"State Count at (i={iterations}): {stateCount}")
