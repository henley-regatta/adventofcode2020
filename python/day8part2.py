#!/usr/bin/python3
#
# My solution for Day 8 Part 2
#
# PROBLEM:
#     Given a simple machine code system with 3 instructions:
#       acc <signedInt>   - Add the parameter to the single register, ACC
#       jmp <signedInt>   - Move execution <signedInt> steps forward/backward
#       nop <signedInt>   - Do nothing, step to next instruction.
#
#    ... Change the value of just one "jmp" or "nop" instruction (by inverting
#        "jmp" to "nop" or vica-versa with the same parameters) such that the
#        program terminates (jumps/advances beyond the instruction set). Report
#        the value of ACC immediately prior to termination.
# DISCUSSION:
#      * There is no point changing "jmp" or "nop" instructions that were never
#      visited by the original looping code (as they cannot affect the outcome)
import sys



###############################################################################
#Load the code into a numbered array of <x>,<ins>,<parm>
def loadInstructions(pfile) :
    instructions=[]
    with open(pfile,"r") as cf:
        for cl in cf:
            part=cl.split()
            instructions.append({'ins' : part[0], 'parm' : int(part[1]), 'visited' : False})
    return instructions

###############################################################################
# YAY A Virtual Machine!
def executeJVM(instructions) :
    #I guess this is a VM, of sorts....
    acc=0   # Accumulator
    pcr=0   # Program Counter
    looped=False
    maxIns=len(instructions)
    #reset visited markers
    for ins in instructions:
        ins['visited']=False
    #Execute the code
    while not looped :
        if pcr>=maxIns:
            break # Normal termination signalled by running off the end of the instruction set
        else:
            #LOAD
            ins=instructions[pcr]
        #LOOP CHECK
        if ins['visited'] :
            looped=True
        else :
            instructions[pcr]['visited']=True
            if ins['ins'] == 'acc' :
                acc = acc + ins['parm']
                pcr = pcr + 1
            elif ins['ins'] == 'jmp' :
                pcr = pcr + ins['parm']
            elif ins['ins'] == 'nop' :
                pcr = pcr + 1
            else :
                print("Invalid instruction at {}; {}".format(pcr,ins))

    return looped,acc,pcr,instructions

###############################################################################
###############################################################################
###############################################################################
if __name__ == "__main__" :
    codefile="../data/day8_input.txt"
    srcCode = loadInstructions(codefile)
    print("Read file containing {} instructions".format(len(srcCode)))
    #Execute the code once, to get a list of instructions that have been visited
    looped,acc,pcr,visitedInstructions = executeJVM(srcCode)
    if looped :
        print("Original execution looped at ins {}".format(pcr))
    else :
        print("oh god something went wrong, didn't loop on original code")
        exit(1)
    #Construct a candidate list of "jmp" and "nop" instructions to change by looking
    #through the visitedInstructions list for ones that have been executed:
    candChng = []
    for i in range(len(visitedInstructions)) :
        if visitedInstructions[i]['visited'] and visitedInstructions[i]['ins'] != "acc" :
                candChng.append(i)
    print("Found {} candidate instructions to swap".format(len(candChng)))

    for i in candChng :
        orgIns=srcCode[i]['ins']
        if orgIns=="nop" :
            srcCode[i]['ins']="jmp"
        elif orgIns=="jmp" :
            srcCode[i]['ins']="nop"
        else :
            print("OH GOD I MESSED UP: INS {} ISN'T A NOP/JMP, ITS: {}".format(i,srcCode[i]))
            exit(2)
        #print("Testing change ins {} from {} -> {}".format(i,orgIns,srcCode[i]['ins']))
        looped,acc,pcr,visitedInstructions = executeJVM(srcCode)
        if looped :
            #print("Test ins {} swap failed; looped at {}".format(i,pcr))
            srcCode[i]['ins']=orgIns #PUT IT BACK BECAUSE SINGLE CHANGES
        else :
            print("Success! Swapping instruction {} ({} to {}) resulted in termination, ACC = {}".
                format(
                    i,
                    orgIns,
                    srcCode[i]['ins'],
                    acc)
            )
            exit(0)
