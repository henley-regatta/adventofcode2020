#!/usr/bin/python3
#
#  My answer for Day 12 Part 2
#
# PROBLEM:
#     Given a list of input instructions of form <I><Distance/Degrees>, where
#        I = N (North)| S (South) | E (East) | W (West)
#        I = L (Left) | R (Right) | F (Forward)
#
#     WHERE ALL INSTRUCTIONS REFER TO THE RELATIVE POSITION OF A WAYPOINT,
#     (N/E/S/W move the waypoint those positions, L/R rotate the waypoint about
#     the ship position)
#     with the exception of F which moves the ship to the waypoint <n> times
#    (the waypoint maintains it's relative position to the ship at all times)
#     And a starting position of (0,0), facing East, waypoint at (10 east, 1 north):
#        a) Calculate the final position by following the instructions
#        b) Compute the "Manhattan Distance" (sum of absolute east/west + north/south positions)
#
#   NOTE: Rotating a vector needs Maths. If you're doing it properly. But we can
#         cheat because all the angles given are multiples of 90 degrees. Fortunately.
import sys
import copy

################################################################################
def parse_instruction(txt) :
    retIns = { 'ins' : "X", 'parm': 0}
    txt = txt.strip()
    if len(txt) > 0 :
        retIns['ins'] = txt[0]
        retIns['parm'] = int(txt[1:])

    return retIns
################################################################################
def rotateWaypoint(inState,dir,degrees) :
    #This would be tough and require some real Trig if the input contained
    #anything other than multiples of 90 degrees. But it doesn't, so we can
    #cheat :-)
    outState = copy.copy(inState)

    #First, simplify the direction:
    if degrees==270 :
        degrees=90
        if dir=="L" :
            dir="R"
        elif dir=="R" :
            dir="L"

    #Now implement the transformation on the waypoint:
    if degrees==180 :
        outState['wpNorth'] = -1 * inState['wpNorth']
        outState['wpEast']  = -1 * inState['wpEast']
    elif degrees==90 and dir=="L" :
        outState['wpNorth'] = inState['wpEast']
        outState['wpEast']  = -1 * inState['wpNorth']
    elif degrees==90 and dir=="R" :
        outState['wpNorth'] = -1 * inState['wpEast']
        outState['wpEast']  = inState['wpNorth']
    else :
        print(f"ARRRRGH unsupported rotation {dir}{degrees}")

    return outState

################################################################################
def update_state_vector(inState,ins) :
    outState = copy.copy(inState)
    if ins['ins'] == 'N' :
        outState['wpNorth'] = inState['wpNorth'] + ins['parm']
    elif ins['ins'] == 'E' :
        outState['wpEast'] = outState['wpEast'] + ins['parm']
    elif ins['ins'] == 'S' :
        outState['wpNorth'] = outState['wpNorth'] - ins['parm']
    elif ins['ins'] == 'W' :
        outState['wpEast'] = outState['wpEast'] - ins['parm']
    elif ins['ins'] == 'L' or ins['ins'] == 'R' :
        #These are the complex instructions in Part 2. Requires translating
        #the Waypoint around the ship by L/R <degrees>
        outState = rotateWaypoint(inState,ins['ins'],ins['parm'])
    elif ins['ins'] == 'F' :
        #This is the only time the ship moves in Part 2. Move by
        #offset waypoint coordinates X times:
        outState['shipNorth'] = inState['shipNorth'] + (ins['parm'] * inState['wpNorth'])
        outState['shipEast']  = inState['shipEast'] + (ins['parm'] * inState['wpEast'])

    else :
        print(f"Argh, unsupported instruction {ins['ins']}")

    return outState

################################################################################
################################################################################
################################################################################
if __name__ == "__main__":
    stateVector = { 'shipNorth': 0, 'shipEast': 0, 'wpNorth': 1, 'wpEast': 10 }

    infile = "../data/day12_input.txt"
    #infile = "../data/day12_test.txt"

    validInstructions = 0
    with open(infile,"r") as insfl :
        for ins in insfl :
            instruction=parse_instruction(ins)
            if instruction['ins'] == "X" : continue #duff instruction
            validInstructions = validInstructions + 1
            print(f"({instruction['ins']}{instruction['parm']:4})",end='->')
            stateVector = update_state_vector(stateVector,instruction)
            print(stateVector)

    print(f"Final State Vector after {validInstructions} instructions",end=': ')
    print(stateVector)
    print("Manhattan Distance: {}".format(abs(stateVector['shipNorth'])+abs(stateVector['shipEast'])))
