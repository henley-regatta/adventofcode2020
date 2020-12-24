#!/usr/bin/python3
#
# My working for Day 23 Part 2
#
# PROBLEM: Play Crab Cups with some made-up complexities -
#          a million cups over ten million rounds.
#
#   Given an input list of INTs, these represent a "circle" of cups clockwise
#   from the first in the list (modulo arithmetic). The game rules are:
#      * First cup becomes CURRENT.
#      * Cups 2,3,4 are REMOVED from list.
#      * DESTINATION cup selected as <Current LABEL>-1
#            * If DESTINATION was in the REMOVED list, select <Current Label>-2
#              (repeat until matched. Wrap-around as required)
#      * <REMOVED> are then placed immediately *clockwise* of DESTINATION in
#        their original order
#      * CURRENT is selected as next in the list.
import time

cuplist="418976235"
#Demo data
#cuplist="389125467"

debug=False

doBigList=True

#A global dictionary. Order the cups by "which cup is next"
#(Confession: I needed hints to get this far. I have solutions using pop/insert)
#(but list / dict manipulation of 1million elements is too slow)
cupLinkedList={}

#Some global metadata. Expect "min", "max" and "num"
cMeta={}

################################################################################
#Play the game via the miracle of linked lists.
def play_crabcups_ll(current) :
    global cupLinkedList
    global cMeta
    #Because the LL is naturally circular, this is easy. As long as you remember
    #to move current's pointer.....
    removed=[]
    nr=cupLinkedList[current]
    for i in range(1,4) :
        removed.append(nr)
        nr=cupLinkedList[nr]
    cupLinkedList[current]=nr
    if debug: print(f" current={current}, removed={removed}")

    #Work out what the "result" cup is. All we need is the min, max and removed list.
    founddest=False
    dest_cup_label=current
    while not founddest :
        if debug : print(f"{dest_cup_label} > {cMeta['min']} ?")
        if dest_cup_label > cMeta['min'] :
            dest_cup_label=dest_cup_label - 1
        else :
            dest_cup_label=cMeta['max']
        if dest_cup_label not in removed :
            founddest=True

    if debug: print(f"Dest: {dest_cup_label}")

    #Now we need to re-arrange the indexes around this dest label
    org_dest_link = cupLinkedList[dest_cup_label]
    nlink=dest_cup_label
    for c in removed :
        cupLinkedList[nlink] = c
        nlink=c
    cupLinkedList[nlink]=org_dest_link

    #Our return value is now simply the value that comes after the one we
    #started with
    return cupLinkedList[current]

################################################################################
# See if you can guess why I need this....
def sanity_check_linked_list(checkmylist) :
    expectedHops=len(checkmylist.keys())
    if debug : print(f"VALIDATING Linked List {checkmylist}")
    posZero = checkmylist[1] #Dodgy assumption but we'll make it anyway
    hops=1
    posFinal = checkmylist[posZero]
    if debug : print(f"\tFirst Hop goes {posZero}->{posFinal}")
    while hops<(expectedHops-1):
        if debug : print(f"\tHop {hops} goes from {posFinal}",end='->')
        posFinal=checkmylist[posFinal]
        if debug : print(posFinal)
        if posFinal == posZero :
            print(f"ERROR Validating linked list. Reached {posZero} after only {hops} steps instead of {expectedHops}")
            return False
        hops+=1
    if checkmylist[posFinal] == posZero :
        print(f"Linked List validated OK, {hops} steps got us back to {posZero}")
        return True
    else :
        print(f"Linked list failed validation; {hops} steps didn't get back to {posZero}")
        return False

################################################################################
def partOneAnswer(llist,start) :
    n=llist[start]
    out=""
    while n != start :
        out+=str(n)
        n=llist[n]
    return str(n)+out

################################################################################
################################################################################
################################################################################
if __name__ == '__main__':
    #max/min values useful to cache to enable wrap-around
    cuplist=[int(i) for i in list(cuplist)]

    cMeta['min']=min(cuplist)
    cMeta['max']=max(cuplist)
    #The internet tells me the right way to do this is a dict of cupbylabel->nextcup
    cupZero = cuplist[0]
    cupLinkedList[cupZero] = cuplist[1]
    for c in range(2,len(cuplist)) :
        cupLinkedList[cuplist[c-1]] = cuplist[c]

    v=cuplist[len(cuplist)-1]

    if doBigList :
        if debug: print(f"Extending {cupLinkedList} to 1,000,000 entries....")
        vNext=cMeta['max']+1
        for c in range(len(cupLinkedList.keys())-1,999998) :
            cupLinkedList[v]=vNext
            cMeta['max']=vNext
            v=vNext
            vNext+=1

    #Loop back to zero
    cupLinkedList[v]=cupZero
    cMeta['num']=len(cupLinkedList.keys())

    if debug :
        print(f"Last V = {v}; links back to {cupLinkedList[v]}")
        for c in list(cupLinkedList.keys())[0:20] :
            print(f"{c} -> {cupLinkedList[c]}")
        if debug: print(f"Cuplist metadata: {cMeta}")

    round=0
    maxRounds=10000000

    current=cuplist[0]
    tStart = time.time()
    while round < maxRounds :
        round+=1
        if debug:
            print("-"*20, "ROUND ", round, " ", "-"*20)
            print(f"{round} : ",end='')
            print(partOneAnswer(cupLinkedList,current),end="->")
        current = play_crabcups_ll(current)
        if debug: print(partOneAnswer(cupLinkedList,current))

    tEnd = time.time()

    tDiff = tEnd - tStart
    tRate = maxRounds / tDiff
    ttComplete = tDiff * (10000000 / maxRounds)
    print(f"(elapsed time: {tDiff:3.3f}, turns/sec: {tRate:1.2f})")
    print(f"Estimated time to complete 100,000,000 rounds: {ttComplete:1.2f} seconds")
    print(f"({ttComplete/3600:1.2f} Hours; {ttComplete/86400:1.2f} Days)")

    #Sanity check the resulting list
    if sanity_check_linked_list(cupLinkedList) :
        #Thanks to this being linked list, working out what's after 1 is stupidly easy:
        ansp1 = cupLinkedList[1]
        ansp2 = cupLinkedList[ansp1]
        ans_product = ansp1 * ansp2

        print(f"The numbers next to cup 1 after {round} rounds are {ansp1} and {ansp2}")
        print(f"The answer to Part Two is therefore {ans_product}")

        #Part one answer:
        #print(f" Part One list: {cupLinkedList}")
        #p1answer=partOneAnswer(cupLinkedList,1)
        #print(f" Part One Answer: {p1answer}")
