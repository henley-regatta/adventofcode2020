#!/usr/bin/python3
# My working for day 1 part 2
#
# PROBLEM: Given a list of <policy> : <password> tuples work out how many
#          passwords in a list are valid/invalid
#          <policy> looks like <num>-<num> <char>
#          where <num>-<num> defines the number of times that <char> must appear
#          in the <password> that follows.
import sys
import json

pwdlist = []
compliant = 0
noncompliant = 0
with open('../data/day2_input.txt','r') as pfile:
    for l in pfile:
        parts = l.split(': ')
        passwd = parts[1]
        pol = parts[0].split()
        pchar = pol[1]
        range = pol[0].split('-')
        min=int(range[0])
        max=int(range[1])
        numOccurrences=passwd.count(pchar)
        pwdlist.append({'min' : min, 'max' : max, 'pchar' : pchar, 'passwd' : passwd, 'occurrences': numOccurrences})
        if numOccurrences >= min and numOccurrences <= max :
            compliant = compliant + 1
        else :
            noncompliant = noncompliant + 1

print("Read {0} passwords. {1} complied with policy ({2} didn't)".format(len(pwdlist),compliant,noncompliant))

with open('../data/day2_input_parsed.json','w') as j:
    json.dump(pwdlist,j)
