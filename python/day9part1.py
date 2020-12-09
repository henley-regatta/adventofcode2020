#!/usr/bin/python3
#
# My solution for Day 9 Part 1
#
# PROBLEM:
#     Given an "XMAS" Cypher that operates as:
#      - Receive a preamble of "Y" (=25 in this problem) numbers
#      - All numbers after this preamble should be the sum of 2
#        distinct numbers in the preceeding Y numbers
#
#      Report the first number in the input that does NOT conform
#      to this criteria.

import sys

inputf = "../data/day9_input.txt"

#This would appear to be static but it'd be nice to change it
lookback=25-1  #0-indexing
pcr=0
gotpreamble=False
numarray = []

############################################################################################
def is_factored(num,numarray) :
    if len(numarray) != lookback+1 :
        print("ERROR called with invalid array length {} abort".format(len(numarray)))
        exit(1)
    for i in range(len(numarray)) :
        for j in range(len(numarray)) :
            if i == j :
                continue
            if numarray[i]+numarray[j] == num :
                return i,j
    return -1,-1
############################################################################################

lc=0
with open(inputf,"r") as f:
    for n in f:
        digit=int(n)
        lc = lc+1
        if gotpreamble :
            i,j = is_factored(digit,numarray)
            if i==-1 and j==-1 :
                print("The {} digit, {}, is not factored by the previous {} numbers".format(lc,digit,lookback+1))
                break
            else :
                print("The {} digit, {}, is factored by digits {},{} ({},{})".format(lc,digit,i,j,numarray[i],numarray[j]))
            numarray[pcr]=digit
        else :
            numarray.append(digit)
        pcr=pcr+1
        if pcr>lookback :
            gotpreamble=True
            pcr=0
