#!/usr/bin/python3
#
#  My solution for Day 10 Part 1
#
#  PROBLEM
#    Given a range of "joltage adapters" having a defined output "joltage"
#    and with the characteristic that each can take an input of 1-3 "jolts"
#    lower than rated voltage, work out the range of joltage differences
#    between the wall (0 jolts) and your device (output = largest adapter
#    joltage + 3 ) when using all adapters.
#
#    Calculate the number of adapters with a difference of 1-jolt, and
#    the number with 3-jolt differences. The answer is the product of those
#    two numbers.



import sys

datafile="../data/day10_input.txt"
#datafile="../data/day10_test1.txt"
#datafile="../data/day10_test2.txt"

adapters=[]
with open(datafile,"r") as af:
    for j in af:
        adapters.append(int(j))

adapters = sorted(adapters)
#We actually always want to count the device as an adapter for accounting purposes so add it
#as the last element to the chain with appropriately defined joltage:
adapters.append(adapters[len(adapters)-1]+3)
chainLength = len(adapters)
print("Read {} adapters+device with a maxJolts of {}.".format(len(adapters),adapters[len(adapters)-1]))

############################################################################################################
#At each stage "n", the acceptable adapters are those with Joltage[n+1] = [Joltage[n]-1, Joltage[n]-2, Joltage[n]-3]
def link_nextstage_chain(inputchain,remainingadapters,num1Jolts,num3Jolts) :
    inJolts=0
    if len(inputchain)>0 :
        inJolts = inputchain[len(inputchain)-1]
    if len(inputchain) == chainLength :
        print("Chain Length: {}. Chain: {}".format(len(inputchain),inputchain))
        print("(Remaining adapters: {})".format(remainingadapters))
        print("End of chain. Final voltage:{}. 1-Jolt steps: {}. 3-Jolt steps: {}. Answer You Seek: {}".format(
            inJolts,
            num1Jolts,
            num3Jolts,
            num1Jolts * num3Jolts))
        exit(0)
    elif len(remainingadapters) == 0 :
        print("Oooh this is bad. Ran out of input adapters without finding a solution. Abort!")
        print("Chain So Far (len={}): {}".format(len(inputchain),inputchain))
        exit(1)
    else :
        for a in remainingadapters :
            if a > inJolts and a <= inJolts+3 :
                #Test this candidate
                tChain=inputchain
                tChain.append(a)
                rChain=remainingadapters
                rChain.remove(a)
                if a==inJolts+1 :
                    link_nextstage_chain(tChain,rChain,num1Jolts+1,num3Jolts)
                elif a==inJolts+3 :
                    link_nextstage_chain(tChain,rChain,num1Jolts,num3Jolts+1)
                else :
                    link_nextstage_chain(tChain,rChain,num1Jolts,num3Jolts)

    print("BACKTRACK at depth {}".format(len(inputchain)))
    return



############################################################################################################
link_nextstage_chain([],sorted(adapters),0,0)
