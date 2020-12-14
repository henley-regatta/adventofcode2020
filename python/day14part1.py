#!/usr/bin/python3
#
# My answer for Day 14 Part 1. Need this to restore my self-confidence a little.
#
#  PROBLEM:
#      Given an input consisting of a Bitmask and a series of memory addresses,
#      work out the sum of all values left in memory after initialization completes.
#
#      Memory values and locations are specified as Decimal.
#
#      Bitmasks are a series of 36 marks of X (ignore), 0 (set bit to 0) or 1
#      (set bit to 1)
#
#     Initialization consists of applying the Bitmask to all values about to be
#     written as memory values.
#
#  NOTES:
#     I'm not using Python's inbuilt bitwise operators because I have no idea
#     what bitlength they are. This has inevitably made my code worse.....
import sys

################################################################################
def read_initialisation_program(infile) :
    outIns = []
    anIns = {}
    with open(infile,"r") as insfl:
        for l in insfl:
            p = l.split(" = ")
            if p[0] == "mask" :
                #write previous ins if exists
                if "mask" in anIns :
                    outIns.append(anIns)
                #Reset the being-read instruction:
                anIns = { 'mask' : p[1].strip(),
                          'memaddrs' : []
                }
            else :
                # All to avoid a simple regular expression....
                v=p[0].split("[")
                a=v[1].split("]")
                anIns['memaddrs'].append([int(a[0]),int_to_bittxt(int(p[1]))])
        #Push the last instruction onto the stack
        outIns.append(anIns)

    return outIns

################################################################################
# TODO: Er, there's probably a native way of achieving the same effect but hey.
# (My god am I rusty on this sort of thing. This is a  horrible algorithm.)
def int_to_bittxt(inputInt) :
    bit=35
    outList=[]
    while bit>-1 :
        p = 2**bit
        d = inputInt // p
        b='X' #How will we know we've mucked up later? Our mem numbers will have this in them.
        if d > 0 :
            b = '1'
            inputInt -= p
        else :
            b = '0'
        outList.append(b)
        bit -=1
    return "".join(outList)

################################################################################
# See above.
def bittxt_to_int(inputTxt) :
    outInt=0
    pos=35
    while pos>-1 :
        if inputTxt[pos]=='1' :
            outInt += 2**(35-pos)
        pos -=1
    return outInt

################################################################################
# Apply the bitmask to an input var
def apply_bitmask_to_txtint(bitmask,txtint) :
    outint=[]

    for p in range(len(bitmask)) :
        if bitmask[p] != 'X' :
            outint.append(bitmask[p])
        else :
            outint.append(txtint[p])
    return "".join(outint)

################################################################################
# Execute an instruction
def execute_instruction(mem,ins) :
    for m in ins['memaddrs'] :
        mem[m[0]] = apply_bitmask_to_txtint(ins['mask'],m[1])
    return mem

################################################################################
################################################################################
################################################################################
if __name__ == '__main__' :
    instructions=read_initialisation_program("../data/day14_input.txt")
    print("Read {} instructions".format(len(instructions)))

    #Let's run thru the sample txt
    #instructions = [{'mask' : 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
    #    'memaddrs' : [
    #        [8,int_to_bittxt(11)],
    #        [7,int_to_bittxt(101)],
    #        [8,int_to_bittxt(0)]
    #    ]
    #}]

    #Memory is an assoc array now...
    memory = {}
    for ins in instructions :

        memory = execute_instruction(memory,ins)

    #The Post-processing step is to convert memory back to int() and report
    #the SUM of all memory addresses:
    runningTotal=0
    for i in sorted(memory.keys()) :
        v=bittxt_to_int(memory[i])
        runningTotal += v

    print(f"The Answer You Seek To Part One Is: {runningTotal}")
