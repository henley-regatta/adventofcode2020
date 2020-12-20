#!/usr/bin/python3
#
# My Working for Day 19 Part 2
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
#        NOTE: 2 MESSAGE RULES ARE RECURSIVE:
#            8: 42 | 42 8
#           11: 42 31 | 42 11 31
#
#
#        MESSAGES then just look like strings of characters to which the rules
#        must be applied.
#
#        QUESTION: How many messages completely match rule 0 ?
import sys

datafile = "../data/day19_input.txt"
#datafile = "../data/day19_test.txt"
#datafile = "../data/day19_test2.txt"


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
    #acceptable_messages = get_tails(0)
    #print(f"There are {len(acceptable_messages)} acceptable messages according to Part1 Processing.")

    #PART 2 FINAGLING: Rules 42 and 31 become psuedo-infinitely repeated given
    #                  the rule 8 and rule 11 changes.
    #  HOWEVER... Rule 0 is the only rule that mentions 8 & 11 meaning that
    #             this (potential) recursion is front-loaded. Solutions that
    #             deal with this as "potential infinite repetition of these patterns,
    #             followed by the remaining stuff" will be adequate *for this case*
    #             Each sub-tail of 31 and 42 is 8 chars long, so acceptable  char lengths
    #             will be
    print(f"Rule 0: 8 11")
    print(f"Rule 8: 42 | 42 8")
    print(f"Rule 11: 42 31 | 42 11 31")


    #Output "patterns" are:
    #   2 or more repetitions of the 42 tails (128 of 'em')
    #   + one or more 31-tails (128 of 'em)
    #GIVEN both 42 and 31 tails are 8 chars long,
    #messages must be at least 24 chars long and "grow" by 8 chars at a time.
    # And there must be at least 1 more 42-tail chunk than 31-tail chunk

    r42tails = get_tails(42)
    r31tails = get_tails(31)

    chunkSize = len(r42tails[0]) #Thankfully this is the same for all tails

    goodMessages=[]
    badMessages=[]
    mCount=0
    for m in messages:
        mCount+=1
        #Parse message in chunkSize chunks
        print(f"{mCount:4} |{m}| len={len(m)} ", end="(")
        #split the message into 8-char chunks:
        chunks = [m[i:i+chunkSize] for  i in range(0,len(m), chunkSize)]
        print(f"{len(chunks)}x{chunkSize}-char chunks)")
        if len(chunks[len(chunks)-1]) != chunkSize :
            print("...Message not a multiple of {chunkSize}, Failed")
            badMessages.append(m)
            continue
        #Control vars
        checkingR42Tails=True
        r42Chunks=0
        r31Chunks=0
        for i in range(len(chunks)) :
            print(f"{i}=|{chunks[i]}|",end=",")
            if checkingR42Tails and chunks[i] in r42tails :
                r42Chunks += 1
                print("OK(R42)",end=",")
                continue
            else :
                checkingR42Tails=False
            if not checkingR42Tails and chunks[i] in r31tails :
                r31Chunks += 1
                print("OK(R31)",end=",")
                continue
            else :
                print("FAILED CHECK - Not R31 or R42")
                break
        if (r42Chunks + r31Chunks == len(chunks)) and (r42Chunks > r31Chunks) and (r31Chunks > 0):
            print("OK PASSED CHECKS")
            goodMessages.append(m)
        else :
            print(f"NO NO FAILED CHECKS because ({r42Chunks}+{r31Chunks} != {len(chunks)}) or ({r42Chunks} <= {r31Chunks}) or ({r31Chunks} == 0)")
            badMessages.append(m)


    print(f"Of the {len(messages)} messages checked, {len(badMessages)} failed but YOUR ANSWER IS {len(goodMessages)}")
