#!/usr/bin/python3
#
# My Answer for Day 24 Part 2
#
# PROBLEM:
#        Given input as a series of instructions of directions to move from
#        a "reference tile" as E, SE, SW, W, NW, NE, with each tile starting
#        as white, flipping to Black on first visit, White on second and so on.
#
#        Determine the total number of BLACK tiles after completing a list of
#        (undelimited) moves.
#
#        NOW, apply the following daily transformations:
#          a) Any BLACK tile with 0 or >2 adjacent BLACK tiles flips to WHITE
#          b) Any WHITE tile with exactly 2 adjacent BLACK tiles flips to BLACK.
#
#       Note: Growth is allowed on each turn. FFS.

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
    return encodetile([xn,yn,zn])
################################################################################
# Part 2 says we need to calculate adjacency. So be it....
def calculate_adjacency(inStr):
    global adjacentCache
    if inStr not in adjacentCache :
        x,y,z=decodetile(inStr)
        ne=encodetile([x+1,y,z-1])
        e =encodetile([x+1,y-1,z])
        se=encodetile([x,y-1,z+1])
        sw=encodetile([x-1,y,z+1])
        w =encodetile([x-1,y+1,z])
        nw=encodetile([x,y+1,z-1])
        adjacentCache[inStr]=[ne,e,se,sw,w,nw]
    return adjacentCache[inStr]

################################################################################
#As we expand we need to initialise tiles if they don't exist. We can defer this
#to the calculate adjacency colour step.
def count_adjacent_blacks(inStr):
    adjacent_tiles=calculate_adjacency(inStr)
    global tiles
    foundBlackTiles=0
    for adj in adjacent_tiles:
        if adj in tiles :
            foundBlackTiles += tiles[adj]
    return foundBlackTiles

################################################################################
def expand_grid(inStr) :
    adjacent=calculate_adjacency(inStr)
    global tiles
    for a in adjacent:
        if a not in tiles:
            tiles[a]=0

################################################################################
# AND NOW I NEED A DATASTRUCTURE.......
# I'll use 0 for White, 1 for Black.
tiles={}
adjacentCache={}

l='0,0,0'
tiles[l] = 0

#Each INSTRUCTION consists of a set of Tile Moves which ends up in a tile that
#instructions=[['nw','w','sw','e','e']]
for instruction in instructions:
    l='0,0,0' #We always start from the origin
    for move in instruction:
        n=apply_move_to_coords(move,l)
        if n not in tiles:
            tiles[n] = 0 #Never visited before, initialise to White.
        l=n
    #At the end of this list we're at "l" and we should invert it's colour
    if tiles[l]==0 :
        tiles[l]=1
    elif tiles[l]==1 :
        tiles[l]=0


blackCount=0
for tile in tiles.keys():
    blackCount += tiles[tile]

print(f"(Part 1 Answer) I found {blackCount} black tiles in the output (from {len(tiles.keys())} total tiles)")

################################################################################
dayCount=0
while dayCount<100 :
    dayCount+=1
    tUpdates={}
    startTiles=list(tiles.keys())
    preGrowth=len(startTiles)
    #Grow and in-fill the grid as necessary
    for t in startTiles:
        expand_grid(t)
    #Re-set the start tiles for the swop count
    startTiles=list(tiles.keys())
    postGrowth=len(startTiles)
    if debug : print(f"{dayCount:2} Grew grid from {preGrowth} to {postGrowth} tiles")
    for t in startTiles:
        bCount=count_adjacent_blacks(t)
        if debug: print(f"{dayCount:2} Tile ({t})[{tiles[t]}] has {bCount} black adjacent tiles",end=":")
        if tiles[t]==0 and bCount==2 :
            #Flip to black
            tUpdates[t]=1
            if debug: print("change to black")
        elif tiles[t]==1 and (bCount==0 or bCount>2) :
            tUpdates[t]=0
            if debug: print("change to white")
        else :
            if debug: print("(no change)")
    #print(f"Day {dayCount} made {len(tUpdates)} tile updates")
    #Now next-state has been calculated, flip the tiles
    if debug: print(f"Day {dayCount:3} updated {len(tUpdates)} of {len(tiles)} tiles")
    for t in tUpdates:
        tiles[t]=tUpdates[t]
    #Cut down on calcs and output for ease of viewing
    #if dayCount%10==0 :
    bc=0
    for tile in tiles.keys():
        bc+=tiles[tile]
    print(f"Day {dayCount:3} has {bc} Black Tiles")

bc=0
for t in tiles.keys() :
    bc+=tiles[t]
print(f"(Part 2 Answer) After {dayCount:3} days there are {bc} Black tiles from {len(tiles)} total")
