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
#    Calculate the number of permutations of adapters that can be used
#    to bridge between input (0 Jolts) and Device (maxAdapter + 3 Jolts) joltage.
#
#    NOTE: Simple algorithms won't scale to the depth of input required. Which
#          is a shame.
import sys

datafile="../data/day10_input.txt"
#datafile="../data/day10_test1.txt"
#datafile="../data/day10_test2.txt"

#Start with the Wall device at Joltage==0
adapters=[0]
with open(datafile,"r") as af:
    for j in af:
        adapters.append(int(j))

print("Input chain: {}".format(adapters))

adapters = sorted(adapters)
#We actually always want to count the device as an adapter for accounting purposes so add it
#as the last element to the chain with appropriately defined joltage:
device=adapters[len(adapters)-1]+3
adapters.append(device)
chainLength = len(adapters)
print("Read {} adapters+device with a maxJolts of {}.".format(len(adapters),adapters[len(adapters)-1]))

#I think we win if we cache sub-chains found from point X, which requires storage
#We win here because Adapters are unique - no two have the same Joltage rating.
#(this would fail if there were duplicates, but then the answer would scale as
# the multiple of adapters-with-same-Joltage anyway)
subCount = {}
for a in adapters :
    if a == device :
        subCount[a]=1
    else :
        subCount[a]=0

############################################################################################################
#Caching previously-calculated subchain permutations lets this algorithm go exponentially faster than
#the naieve approach of re-calculating each permutation individually....
#(this approach wouldn't work if there were "forbidden paths" - sub-chains that don't terminate in the
# target device Joltage. We'd need better error-bounds checking if that were the case)
def get_subCount_from_x(x) :
    global subCount
    if subCount[x]==0 :      #We've already calculated how many permutations *start* from here, return that.
        for c in adapters :
            if c<x+1 or c>x+3: #Skip values outside the "permitted" Joltage range.
                continue
            subCount[x]=subCount[x]+get_subCount_from_x(c)  #Within the permitted range, add all sub-permutations.
    return subCount[x]

############################################################################################################
############################################################################################################
############################################################################################################
print("-"*80)
print("I found {} Permutations of permitted adapter chains".format(get_subCount_from_x(0)))
