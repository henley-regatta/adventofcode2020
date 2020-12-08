#!/usr/bin/python3
#
# My solution for Day 8 Part 1
#
# PROBLEM:
#     Given a simple machine code system with 3 instructions:
#       acc <signedInt>   - Add the parameter to the single register, ACC
#       jmp <signedInt>   - Move execution <signedInt> steps forward/backward
#       nop <signedInt>   - Do nothing, step to next instruction.
#
#    ... find the value of ACC immediately before the program loops (i.e.
#    just before the code goes to infinite repetition)
import sys

#Load the code into a numbered array of <x>,<ins>,<parm>
codefile="day8_input.txt"
instructions=[]
with open(codefile,"r") as cf:
    for cl in cf:
        part=cl.split()
        instructions.append({'ins' : part[0], 'parm' : int(part[1]), 'visited' : False})

print("Read file containing {} instructions".format(len(instructions)))

#I guess this is a VM, of sorts....
acc=0   # Accumulator
pcr=0   # Program Counter
looped=False
while not looped :
    #LOAD
    ins=instructions[pcr]
    if ins['visited'] :
        looped=True
        print("Looping at instruction {}; ACC prior to execution: {}, instruction was: {}".format(pcr,acc,ins))
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
