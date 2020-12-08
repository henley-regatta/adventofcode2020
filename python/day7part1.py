#!/usr/bin/python3
#
# My working for Day 7, part 1
#
# PROBLEM SPEC:
#    Given a list of input rules of the form:
#     <colour> bags contain <x> <colour> bags{, <y> <colour> bags}
#
#    ...Determine the number of <colour> bags that can contain at least one
#       Shiny Gold bag (either directly or indirectly)
import sys
import re

#Input rules match one of two forms:
simprule = re.compile('(.+) bags contain ([0-9]+) (.+) bag')
comprule = re.compile('\D+([0-9]+) (.+) bag')
nocontains = re.compile('(.+) bags contain no other')

#Read the list of rules in from file
bagrules = {}
rfile="../data/day7_input.txt"
#rfile="d7_test.txt"
with open(rfile,"r") as rf:
    for rtext in rf:
        rule = {}
        contains = {}
        rparts=rtext.split(",")
        #First entry MUST exist and is the simple rule
        m = re.match(simprule,rparts[0])
        if m :
            col=m.group(1)
            contains[m.group(3)] = m.group(2)
            for rpart in rparts[1:len(rparts)]:
                o = re.match(comprule,rpart)
                if o:
                    contains[o.group(2)] = o.group(1)
        else :
            m = re.match(nocontains,rparts[0])
            if m :
                col=m.group(1)
            else :
                print("FAILED MATCH: {0}".format(rtext))
        bagrules[col] = contains

print("{0} Bag-contains rules found".format(len(bagrules)))

#Strictly speaking we now wish to invert the built structure to find the
#set of bags which can contain, directly or indirectly, our target "shiny gold"
#bag.

def colIsContainedBy(bagrules,desiredCol) :
    isContainedBy = []
    for col in bagrules.keys() :
        for bc in bagrules[col].keys() :
            if bc == desiredCol :
                isContainedBy.append(col)
    return isContainedBy

directContains = colIsContainedBy(bagrules,"shiny gold")

contCount = len(directContains)
print("{} direct contains:{}".format(contCount,directContains))
#Now we have a bunch of levels of indirection to look for.
alreadycounted = { i : 1 for i in directContains }
searchlist = directContains
while len(searchlist) > 0 :
    ccol=searchlist.pop()
    indCont = colIsContainedBy(bagrules,ccol)
    for iC in indCont :
        if iC not in alreadycounted :
            contCount = contCount + 1
            searchlist.append(iC)
            alreadycounted[iC] = 1

print("Recursive Search found a total of {0} direct/indirect contains".format(contCount))
