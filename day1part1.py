#!/usr/bin/python3
# My working for day 1 part 1
#
# PROBLEM: Given a list of input numbers, work out which pair sum to 2020
#          Calculate the product of that pair as the result.
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
        if i != j : #don't compare same number twice
            if x + numlist[j] == 2020:
                print("elem {0} - {1} and {2} - {3} sum to 2020 with product {4}".format(i,x,j,numlist[j], x*numlist[j]) )
