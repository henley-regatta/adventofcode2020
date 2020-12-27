#!/usr/bin/python3
#
# My Answer for Day 24 Part 1
#
# PROBLEM:
#        Given input as a series of instructions of directions to move from
#        a "reference tile" as E, SE, SW, W, NW, NE, with each tile starting
#        as white, flipping to Black on first visit, White on second and so on.
#
#        Determine the total number of BLACK tiles after completing a list of
#        (undelimited) moves.
import sys

debug=False

datafile="../data/day24_input.txt"
#datafile="../data/day24_test.txt"

#Input isn't delimited and is variable width. Luckily, if it starts N or S it
#MUST be followed by E or W, but if it starts E/W it's single-char.
instructions=[]
with open(datafile,"r") as tf:
    for l in tf:
        tileJumps=[]
        lastc=''
        lc=list(l.strip().lower())
        for c in lc :
            if c == 'n' or c =='s' :
                lastc=c
            elif lastc != '' :
                tileJumps.append(lastc+c)
                lastc=''
            else :
                tileJumps.append(c)
        instructions.append(tileJumps)

print(f"Read a list of {len(instructions)} instructions from the file:")

################################################################################
def decodetile(tileStr) :
    x,y,z=tileStr.split(',')
    return [int(x),int(y),int(z)]
################################################################################
def encodetile(tileCoord) :
    x=str(tileCoord[0])
    y=str(tileCoord[1])
    z=str(tileCoord[2])
    return ','.join([x,y,z])

################################################################################
#Hex grids are used a lot in games. This page: https://www.redblobgames.com/grids/hexagons/
#describes how. Thinking of them as 2-d projections of cubes helped me. With "pointy"
#hexagons we define +z as N, +x as NE and +y as NW and maintain the property x+y+z=0
# IF I start at (0,0,0) then the moves are:
#   NE: (+1,0,-1)
#    E: (+1,-1,0)
#   SE: (0,-1,+1)
#   SW: (-1,0,+1)
#    W: (-1,+1,0)
#   NW: (0,+1,-1)
def apply_move_to_coords(ins,lastStr) :
    xp,yp,zp=decodetile(lastStr)
    if ins == 'ne' :
        xn=xp+1
        yn=yp
        zn=zp-1
    elif ins == 'e' :
        xn=xp+1
        yn=yp-1
        zn=zp
    elif ins == 'se' :
        xn=xp
        yn=yp-1
        zn=zp+1
    elif ins == 'sw' :
        xn=xp-1
        yn=yp
        zn=zp+1
    elif ins == 'w' :
        xn=xp-1
        yn=yp+1
        zn=zp
    elif ins == 'nw' :
        xn=xp
        yn=yp+1
        zn=zp-1
    else :
        print(f"Unrecognised Move Direction: {ins}")
        exit(2)
    if debug: print(f"({xp},{yp},{zp})->{ins}->({xn},{yn},{zn})")
    return encodetile([xn,yn,zn])
################################################################################
# AND NOW I NEED A DATASTRUCTURE.......
# I'll use 0 for White, 1 for Black.
tiles={}

l='0,0,0'
tiles[l] = 0

#Each INSTRUCTION consists of a set of Tile Moves which ends up in a tile that
#instructions=[['nw','w','sw','e','e']]
for instruction in instructions:
    l='0,0,0' #We always start from the origin
    if debug : print(f"Following a list of {len(instruction)} moves: ",end="")
    for move in instruction:
        n=apply_move_to_coords(move,l)
        if n not in tiles:
            tiles[n] = 0 #Never visited before, initialise to White.
        l=n
    #At the end of this list we're at "l" and we should invert it's colour
    tiles[l] = not tiles[l]
    if debug: print(f"Tile moves took us to ({l}) and we changed it to {tiles[l]}")

blackCount=0
for tile in tiles.keys():
    blackCount += tiles[tile]

print(f"I found {blackCount} black tiles in the output (from {len(tiles.keys())} total tiles)")
