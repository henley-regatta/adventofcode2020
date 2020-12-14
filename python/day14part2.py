#!/usr/bin/python3
#
# My answer for Day 14 Part 2. p1 took me ages but was satisfying. What will this be like?
#
#  PROBLEM:
#      Given an input consisting of a Bitmask and a series of memory addresses,
#      work out the sum of all values left in memory after initialization completes.
#
#      Memory values and locations are specified as Decimal.
#
#      Bitmasks are a series of 36 marks of X (Float), 0 (leave input alone) or 1
#      (set bit to 1)
#
#     Initialization consists of applying the Bitmask to all Memory Addresses
#     before writing.Floating bits (X) on the bitmask mean "all possible values",
#     which means as well as modifying the address written, there will be MULTIPLE
#     addresses written for a given input.
#
#  NOTES:
#     I'm not using Python's inbuilt bitwise operators because I have no idea
#     what bitlength they are. This has inevitably made my code worse.....
#
#     I wasted HOURS on trying to be clever about this, assuming that high-order
#     X's in the bitmasks would result in billions of memory writes. But I
#     was wrong because the total number of X's in any given row is relatively low.
#
#     So it's quicker to just execute the instructions than do any overlap calculation.

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
                anIns['memaddrs'].append([int(a[0]),int(p[1])])
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
# Apply the bitmask to a memory address using the X=Float rule
def apply_bitmask_to_memaddr(bitmask,inaddr) :
    outaddr = []
    inaddrBitText = int_to_bittxt(inaddr)
    outMask = []
    for p in range(len(bitmask)) :
        if bitmask[p] == '0' :
            outMask.append(inaddrBitText[p])
        else :
            outMask.append(bitmask[p])
    return "".join(outMask)


################################################################################
# Execute an instruction. Part2 is more complex, because shoving in a single
# address will cause at least one but probably many addresses to be spat back.
def execute_instruction(mem,ins) :
    for m in ins['memaddrs'] :
        outMask = apply_bitmask_to_memaddr(ins['mask'],m[0])
        outAddrCount = calc_instr_count(outMask)
        mem.append([outMask,outAddrCount,m[1]])
    return mem

################################################################################
# helper/display function for checking my working.
# Oh god I am not a smart man.
def enumerate_addr(memmask) :
    #Pass one: get a "base Address" by substituting all X's for 0:
    baseAddr=0
    x=len(memmask)-1
    maxX=x
    baseAddr=0
    while x>-1 :
        if memmask[x]=='1' :
            baseAddr += 2**(maxX-x)
        x -= 1
    #Pass two: Extend the list by the bit-position for each X:
    x=maxX
    outVals=[baseAddr]
    while x>-1 :
        if memmask[x]=='X' :
            existingNums=len(outVals)
            for i in range(existingNums) :
                v = outVals[i] + 2**(maxX-x)
                outVals.append(v)
        x -= 1
    return outVals

################################################################################
#Work out how many instructions an "X"-masked memory address applies to:
def calc_instr_count(memmask) :
    xCount=0
    for b in memmask :
        if b == "X" :
            xCount += 1
    return 2**xCount


################################################################################
################################################################################
################################################################################
if __name__ == '__main__' :

    #Let's run thru the sample txt:
    instructions = [
        {   'mask' : '000000000000000000000000000000X1001X',
            'memaddrs' : [
                [42,100],
            ]
        },
        {   'mask' : '00000000000000000000000000000000X0XX',
            'memaddrs' : [
                [26,1],
            ]
        },
        {   'mask' : '00000000000000000000000000000000X0XX',
            'memaddrs' : [
                [63,10],
            ]
        },
    ]

    instructions=read_initialisation_program("../data/day14_input.txt")
    print("Read {} instructions".format(len(instructions)))

    #We need to process memory in order now to determine final update.
    memory = []
    for ins in instructions :
        memory = execute_instruction(memory,ins)

    #Work out how many expected "memory writes" we can expect evaulating this
    #instruction set:
    calcWrites=0
    maxWrites=0
    for m in memory:
        calcWrites += m[1]
        if m[1]>maxWrites :
            maxWrites = m[1]

    numInstr = len(memory)
    avgWritesPerInstr = calcWrites / len(memory)

    #Execution time will scale linearly with the number of calculated Memory
    #writes.... values in the billion here would be bad for performance
    #(and given it's a 36-bit address space, potentially for memory usage too)

    print(f"PREEXEC Caution: {calcWrites} memory writes for {numInstr} values")
    print(f"(average {avgWritesPerInstr:.1f}, max {maxWrites})")

    #"Accumulate" the outputs forward:
    fwdMemMap={}
    overlaps=0
    writes=0
    calcWrites=0
    for m in memory :
        calcWrites += m[1]
        for a in enumerate_addr(m[0]) :
            writes +=1
            if a in fwdMemMap :
                overlaps += 1
            fwdMemMap[a] = m[2]

    #Now we have a complete memory map of the writes we can calculate the output:
    addrs=0
    runningCount=0
    for a in fwdMemMap.keys() :
        addrs+=1
        runningCount += fwdMemMap[a]

    print(f"After {writes} actual from {calcWrites} expected memory writes to a total of {addrs} addresses with {overlaps} overlaps,")
    print(f"The answer you seek is {runningCount}")
    exit(0)
