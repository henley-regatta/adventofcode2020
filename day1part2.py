#!/usr/bin/python3
# My working for day 1 part 2
#
# PROBLEM: Given a list of input numbers, work out which 3 together sum to 2020
#          Calculate the product of that 3 some as the result.
import sys

#Get the input list
numlist = []
with open("day1_input.txt",'r') as numfile:
    for l in numfile:
        numlist.append(int(l))

print("Read {0} entries from numberlist".format(len(numlist)))

#Brute force the list to find the sums.
for i in range(len(numlist)) :
    x = numlist[i]
    for j in range(len(numlist)) :
        y = numlist[j]
        xy = x + y
        if i != j : #don't compare same number twice
            for k in range(len(numlist)) :
                if i != k and j != k : #don't compare the same numbers again
                    if xy + numlist[k] == 2020:
                        print("{0} + {1} + {2} sum to 2020 with product {3}".format(x,y,numlist[k],x*y*numlist[k]))
            
