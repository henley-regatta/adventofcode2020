#!/usr/bin/python3
# My working for day 1 part 2
#
# PROBLEM: Given a list of <policy> : <password> tuples work out how many
#          passwords in a list are valid/invalid
#          <policy> looks like <num>-<num> <char>
#          where <num>-<num> defines the position in the string that <char> must appear
#          in the <password> that follows.
#
# NOTE: Uses parsing from part1 to import json as preparsed.
import sys
import json

with open('../data/day2_input_parsed.json','r') as j:
    pwdlist = json.load(j)

compliant = 0
noncompliant = 0
for p in pwdlist:
    chlist = list(p['passwd'])
    minC = chlist[p['min']-1]
    maxC = chlist[p['max']-1]
    minIsChar = (minC == p['pchar'])
    maxIsChar = (maxC == p['pchar'])
    if (minIsChar and not maxIsChar) or (maxIsChar and not minIsChar):
        compliant = compliant + 1
    else :
        noncompliant = noncompliant + 1

print("Read {0} passwords. {1} complied with policy ({2} didn't)".format(len(pwdlist),compliant,noncompliant))
