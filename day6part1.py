#!/usr/bin/python3
#
# My script for solving Day 6 Part 1
#
# PROBLEM SPEC:
#      Given an input representing the set of questions a-z for which a
#      YES answer was given by a particular person, and for whom groups are
#      made up of sets of person-answers, calculate the GROUP YES score
#      of unique replies.
#      The answer is the sum of all group yes-counts.
#
#      Input represents people-answers one-per-line, with groups separated by
#      a blank line.
import sys


def parse_person_input(person_string) :
    person_key = {}
    for i in range(len(person_string)) :
        person_key[person_string[i]] = 1
    return person_key

#Get our input, split into groups
groupinput=[]
with open("day6_input.txt","r") as input:
    group=[]
    for line in input:
        person=line.strip('\n')
        if len(person)>0 :
            group.append(parse_person_input(person))
        else :
            groupinput.append(group)
            group = []
    #last line
    groupinput.append(group)

#Iterate over the groups, form a group count
gc=[]
for g in groupinput :
    gans={}
    for p in g :
        for a in p :
            if a not in gans :
                gans[a]=1
    gc.append(gans)

print("There are {} groups of people on the flight".format(len(groupinput)))
print("Coalesed to {} groups of answers".format(len(gc)))
ans_count = 0
for g in gc:
    ans_count = ans_count + len(g.keys())

print("Sum of all answers across groups: {0}".format(ans_count))
