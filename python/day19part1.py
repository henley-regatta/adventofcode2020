#!/usr/bin/python3
#
# My Working for Day 19 Part 1
#
# PROBLEM:
#      Given a list of nested rules, verify a number of messages against those
#      rules.
#
#      Rules are of 2 basic forms:
#        SIMPLE:
#           <n>: "X"   - Rule <n> states that the character "X" must match
#        COMPOUND:
#           <n>:  <a> <b> <c> - Rule <n> states that the message must match rule <a> then <b> then <c>
#           <n>:  <b> | <c>   - Rule <n> states that the message must match rule <b> OR <c>
#
#        MESSAGES then just look like strings of characters to which the rules
#        must be applied.
#
#        QUESTION: How many messages completely match rule 0 ?
import sys

datafile = "../data/day19_input.txt"
#datafile = "../data/day19_test.txt"

######################################################################
#Job one is always an input parser....
def readInput(datafile) :
    rules={}
    messages=[]
    foundMessages=False
    with open(datafile,"r") as df:
        for line in df :
            line=line.strip()
            #RULES and MESSAGES are separated by a blank line:
            if len(line)==0 :
                foundMessages=True
                continue
            if foundMessages :
                messages.append(line)
            else :
                r = line.split(':')
                rules[int(r[0])] = { 'txt' : r[1].strip() }

    return rules,messages

######################################################################
# ALWAYS RETURNS A LIST. ALWAYS.
def get_tails(ruleNo) :
    global rules

    #Bit of performance optimisation..... use cached result if available
    if 'tails' in rules[ruleNo].keys() :
        return rules[ruleNo]['tails']

    #Terminals start with '"' followed by a letter
    if rules[ruleNo]['txt'][0] == '"' :
        rules[ruleNo]['tails'] = [rules[ruleNo]['txt'][1]]
        return [rules[ruleNo]['txt'][1]]

    #The "General Case" is a sequence of numbers possibly split by "|"
    subClauses=[]
    rules[ruleNo]['tails'] = []
    for c in rules[ruleNo]['txt'].split() :
        if len(c)>0 :
            if c == "|" :
                #"OR": Save everything we've gathered so far as a list,
                #Blank the list and start again.
                rules[ruleNo]['tails'].extend(subClauses)
                subClauses=[]
            else :
                #A NUMBER. So, recurse to that rule and re-evaluate.
                #Result is ALWAYS A list. So:
                if len(subClauses)==0 :
                    subClauses = get_tails(int(c))
                else :
                    sc = get_tails(int(c))
                    tmpClauses = []
                    if len(sc) > len(subClauses) :
                        for i in range(len(sc)) :
                            for j in range(len(subClauses)) :
                                tmpClauses.append(subClauses[j] + sc[i])
                    else :
                        for i in range(len(subClauses)) :
                            for j in range(len(sc)) :
                                tmpClauses.append(subClauses[i] + sc[j])
                    subClauses = tmpClauses
    rules[ruleNo]['tails'].extend(subClauses)
    return rules[ruleNo]['tails']

######################################################################
######################################################################
if __name__ == '__main__' :
    rules,messages = readInput(datafile)
    print("Found {} messages and {} rules in file {}".format(len(messages),len(rules.keys()),datafile))
    acceptable_messages = get_tails(0)
    print(f"There are {len(acceptable_messages)} acceptable messages")

    isGood = 0
    for m in messages:
        if m in acceptable_messages :
            isGood += 1

    print(f"Of the {len(messages)} messages read, {isGood} match Rule 0")
