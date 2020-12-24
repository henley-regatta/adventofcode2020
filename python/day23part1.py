#!/usr/bin/python3
#
# My working for Day 23 Part 1
#
# PROBLEM: Play Crab Cups
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
import copy

cuplist="418976235"
#Demo data
#cuplist="389125467"

debug=False

################################################################################
def play_crabcups_round(inlist,cIndex,minCup,maxCup) :
    clist=[int(i) for i in list(inlist)]
    cupLength=len(clist)
    current=clist[cIndex]
    if debug: print(f"cIDx:    {cIndex}\nIN:      {clist}\nCURRENT: {current}")
    remain=copy.copy(clist)
    #SETUP THE HAND.......
    #Remove the 3 to the right of cIndex taking into account wrapping at len.
    removed=[]
    #Remove the 3 cups "clockwise" from the current taking into account wrap-around
    i=cIndex
    for j in range(3) :
        i+=1
        if i >= cupLength :
            i=0
        removed.append(clist[i])
    #And now remove them from the remaining list
    if debug: print(f"REMOVED: {removed}")
    for r in removed :
        remain.remove(r)
    if debug: print(f"REMAIN:  {remain}")

    #RIGHT Look for the "target" position into which we'll insert the removed:
    found=False
    search=current
    fpos=-1
    while not found :
        #Handle wrap-around.
        if search > minCup :
            search=search-1
        else :
            search=maxCup
        if search in remain :
            found=True
            fpos = remain.index(search)
    if debug: print(f"TARGET: {search} at POS: {fpos}")

    #DONE. Now build the output list.
    #Start with everything prior to and including target:
    olist=remain[:fpos+1]
    #Insert the removed
    olist += removed
    #And add the rest of the remainder after the found one
    olist += remain[fpos+1:]

    #NOW there's a permutation required to make sure that "current" has the
    #same index position in olist that it had in "ilist" by rotating the
    #array around the right number of places.
    ocIndex=olist.index(current)
    if debug : print(f"currentindex. IN={cIndex} OUT={ocIndex}")
    if ocIndex < cIndex :
        rot=cIndex-ocIndex
        tlist=olist[rot:]
        olist=tlist + olist[:rot]
    elif ocIndex > cIndex :
        rot = ocIndex-cIndex
        tlist=olist[:rot]
        olist=olist[rot:] + tlist

    if debug: print(f"OUT:     {olist}")

    return ''.join([str(i) for i in olist])


################################################################################
################################################################################
################################################################################
if __name__ == '__main__':
    #max/min values useful to cache to enable wrap-around
    tlist=[int(i) for i in list(cuplist)]
    minCup=min(tlist)
    maxCup=max(tlist)
    numCups=len(tlist)-1
    round=1
    cIndex=-1
    while round <= 100 :
        if debug: print("-"*20, "ROUND ", round, " ", "-"*20)
        if cIndex<numCups :
            cIndex+=1
        else :
            cIndex=0
        outlist = play_crabcups_round(cuplist,cIndex,minCup,maxCup)
        print(f"{round}({cIndex}): {cuplist} -> {outlist}")
        cuplist=outlist
        round+=1

    #Calculate final score by reporting the list AFTER one with rotation
    vlist=[int(i) for i in list(cuplist)]
    onePos=vlist.index(1)
    olist=vlist[onePos+1:]
    olist+=vlist[:onePos]
    ostr= "".join([str(i) for i in olist])
    print(f"Answer after {round} rounds = {ostr}")
