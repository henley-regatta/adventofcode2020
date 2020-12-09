#!/usr/bin/python3
#
# My solution for Day 9 Part 2
#
# PROBLEM:
#     Given an "XMAS" Cypher that operates as:
#      - Receive a preamble of "Y" (=25 in this problem) numbers
#      - All numbers after this preamble should be the sum of 2
#        distinct numbers in the preceeding Y numbers
#
#      Report the first number in the input that does NOT conform
#      to this criteria.
#
#      Find a contiguous set of numbers that sum to this non-conforming
#      number.
#
#      Sum the Smallest and the Largest numbers in this contiguous list.
#      Report this number.

import sys

inputf = "../data/day9_input.txt"

lookback=25

############################################################################################
def read_numlist(filename) :
    numlist=[]
    with open(filename,"r") as f:
        for n in f:
            numlist.append(int(n))
    return numlist

############################################################################################
def is_factored(num,numarray) :
    for i in range(len(numarray)) :
        for j in range(len(numarray)) :
            if i == j :
                continue
            if numarray[i]+numarray[j] == num :
                return i,j
    return -1,-1

############################################################################################
# Methodology:  Iterate through the read-in numbers starting after the preamble. Look for
#               the first number that can't be summed by any 2 different numbers in the
#               previous lookback range and return that.
def find_first_unfactored_num(lookback, numlist) :
    for lc in range(lookback,len(numlist)) :
        digit=numlist[lc]
        i,j = is_factored(digit,numlist[(lc-lookback):lc])
        if i==-1 and j==-1 :
            print("The {} digit, {}, is not factored by the previous {} numbers".format(lc,digit,lookback))
            return digit

    print("Error Finding First Unfactored Pair. You Should Not Have Got Here")
    exit(1)

############################################################################################
#Methodology: Start from (startidx) and keep adding the numbers encountered to a running
#             count. If we *exceed* the target value we've failed, return -1. Otherwise,
#             because the end index counts, return that value on matching.
def contiguous_sums_to_value(targetval,startidx,numlist) :
    runningcount=0
    for i in range(startidx,len(numlist)) :
        runningcount=runningcount+numlist[i]
        if runningcount > targetval :
            return -1
        elif runningcount == targetval :
            return i
    print("Error you've run off the end of the number list implying you started too late?")
    exit(2)

############################################################################################
############################################################################################
############################################################################################
if __name__ == "__main__":
    numlist=read_numlist(inputf)
    first_unfactored_num=find_first_unfactored_num(lookback,numlist)
    #This number is the answer to day9part1 if you're interested, fact fans.

    #This is really where Day2 work begins:
    for i in range(len(numlist)) :
        j =  contiguous_sums_to_value(first_unfactored_num,i,numlist)
        if j != -1 :
            contiguous_range = numlist[i:j]
            print("This set starting at i={} sums to {}: {}".format(i,first_unfactored_num,contiguous_range))
            #we want the SMALLEST and LARGEST number in this list so we must first sort it
            sorted = sorted(contiguous_range)
            print("The smallest number is {}, the largest is {} and the sum of these is {}".format(
                sorted[0],
                sorted[len(sorted)-1],
                sorted[0] + sorted[len(sorted)-1]
            ))
            exit(0)

    print("Error if you got here I couldn't find an answer in the given input file ({}) with lookback of {}. Are you sure it's correct?".format(inputf,lookback))
