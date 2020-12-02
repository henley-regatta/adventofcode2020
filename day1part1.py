#!/usr/bin/python3
# My working for day 1 part 1
#
# PROBLEM: Given a list of input numbers, work out which pair sum to 2020
#          Calculate the sum of that pair as the result.
import sys

#Get the input list
numlist = []
with open("day1_input.txt",'r') as numfile:
    for l in numfile:
        numlist.append(int(l))

print("Read {0} entries from numberlist".format(len(numlist)))
