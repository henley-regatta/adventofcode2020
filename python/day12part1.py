#!/usr/bin/python3
#
#  My answer for Day 12 Part 1
#
# PROBLEM:
#     Given a list of input instructions of form <I><Distance/Degrees>, where
#        I = N (North)| S (South) | E (East) | W (West)
#        I = L (Left) | R (Right) | F (Forward)
#
#     And a starting position of (0,0), facing East:
#        a) Calculate the final position by following the instructions
#        b) Compute the "Manhattan Distance" (sum of absolute east/west + north/south positions)
import sys

################################################################################
def parse_instruction(txt) :
    retIns = { 'ins' : "X", 'parm': 0}
    txt = txt.strip()
    if len(txt) > 0 :
        retIns['ins'] = txt[0]
        retIns['parm'] = int(txt[1:])

    return retIns
################################################################################
def move_direction(inState,distance) :
    outState = inState
    #Let's cheat.
    if inState['Heading'] == 0 :
        outState['North'] = outState['North'] + distance
    elif inState['Heading'] == 180 :
        outState['North'] = outState['North'] - distance
    elif inState['Heading'] == 90 :
        outState['East'] = outState['East'] + distance
    elif inState['Heading'] == 270 :
        outState['East'] = outState['East'] - distance
    else :
        print(f"Argh, unsupported heading: {inState['Heading']}")
    return outState

################################################################################
def update_state_vector(inState,ins) :
    outState = inState
    if ins['ins'] == 'N' :
        outState['North'] = outState['North'] + ins['parm']
    elif ins['ins'] == 'E' :
        outState['East'] = outState['East'] + ins['parm']
    elif ins['ins'] == 'S' :
        outState['North'] = outState['North'] - ins['parm']
    elif ins['ins'] == 'W' :
        outState['East'] = outState['East'] - ins['parm']
    elif ins['ins'] == 'L' :
        outState['Heading'] = (outState['Heading'] - ins['parm']) % 360
    elif ins['ins'] == 'R' :
        outState['Heading'] = (outState['Heading'] + ins['parm']) % 360
    elif ins['ins'] == 'F' :
        outState = move_direction(inState, ins['parm'])
    else :
        print(f"Argh, unsupported instruction {ins['ins']}")

    return outState


################################################################################
################################################################################
################################################################################
if __name__ == "__main__":
    stateVector = { 'North': 0, 'East': 0, 'Heading': 90}

    infile = "../data/day12_input.txt"
#    infile = "../data/day12_test.txt"

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
    print("Manhattan Distance: {}".format(abs(stateVector['North'])+abs(stateVector['East'])))
