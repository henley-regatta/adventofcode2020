#!/usr/bin/python3
#
# My working for Day 7, part 2
#
# PROBLEM SPEC:
#    Given a list of input rules of the form:
#     <colour> bags contain <x> <colour> bags{, <y> <colour> bags}
#
#    ...Determine the number of bags required to allow 1 Shiny Gold
#    bag to be carried.
import sys
import re

#Input rules match one of two forms:
simprule = re.compile('(.+) bags contain ([0-9]+) (.+) bag')
comprule = re.compile('\D+([0-9]+) (.+) bag')
nocontains = re.compile('(.+) bags contain no other')

#Read the list of rules in from file
bagrules = {}
rfile="../data/day7_input.txt"
#rfile="../data/d7_test.txt"
#rfile="../data/d72test.txt"
with open(rfile,"r") as rf:
    for rtext in rf:
        rule = {}
        contains = {}
        rparts=rtext.split(",")
        #First entry MUST exist and is the simple rule
        m = re.match(simprule,rparts[0])
        if m :
            col=m.group(1)
            contains[m.group(3)] = int(m.group(2))
            for rpart in rparts[1:len(rparts)]:
                o = re.match(comprule,rpart)
                if o:
                    contains[o.group(2)] = int(o.group(1))
        else :
            m = re.match(nocontains,rparts[0])
            if m :
                col=m.group(1)
            else :
                print("FAILED MATCH: {0}".format(rtext))
        bagrules[col] = contains

print("***{0} Bag-contains rules found".format(len(bagrules)))

#Another form of recursive search, this time starting from X find the sum
#of bags needed to allow an X bag to be carried. NOTE: need to do depth-first
#recursion to calculate "back up the tree" the multiples.

def getSubBagCount(fromBag,bagrules,depth) :
    print("{0}{1}[{2}]:".format("+"*depth,fromBag,bagrules[fromBag]))
    depth = depth+1
    subBagCount = 1 # No matter what else we'll return ourself
    #special (terminating) case
    #if len(bagrules[fromBag].keys()) == 0 :
    #    subBagCount=1
    #else :
    for subBag in bagrules[fromBag] :
        subBags = bagrules[fromBag][subBag] * getSubBagCount(subBag,bagrules,depth)
        print("{0}{1} total subbags".format("-"*depth,subBags))
        subBagCount = subBagCount + subBags

    print("{0} returns {1}".format("-"*depth,subBagCount))
    return subBagCount

totBagCount = getSubBagCount("shiny gold",bagrules,0)-1 #we've over-counted for the head

print("We need {0} total bags.".format(totBagCount))
