#!/usr/bin/python3
#
# My script for solving Day 6 Part 2
#
# PROBLEM SPEC:
#      Given an input representing the set of questions a-z for which a
#      YES answer was given by a particular person, and for whom groups are
#      made up of sets of person-answers, calculate the GROUP YES score
#      as the number of questions for whom ALL MEMBERS answered yes.
#      The answer is the sum of all group yes-counts.
#
#      Input represents people-answers one-per-line, with groups separated by
#      a blank line.
import sys

#Get our input, split into groups
groupinput=[]
with open("../data/day6_input.txt","r") as input:
    group={'pcount':0}
    for line in input:
        person=line.strip('\n')
        if len(person)>0 :
            group['pcount']=group['pcount']+1
            for i in range(len(person)) :
                ans=person[i]
                if ans in group :
                    group[ans] = group[ans] + 1
                else :
                    group[ans] = 1
        else :
            groupinput.append(group)
            group = {'pcount':0}
    #last line
    groupinput.append(group)

print("There are {} groups of people on the flight".format(len(groupinput)))

ans_count = 0
for g in groupinput:
    groupyes=0
    for a in g.keys() :
        if a != 'pcount' and g[a] == g['pcount'] :
            groupyes=groupyes+1
    ans_count = ans_count + groupyes

print("Sum of all answers across groups: {0}".format(ans_count))
