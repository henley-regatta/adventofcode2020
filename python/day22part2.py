#!/usr/bin/python3
#
# My working for day 22 part 2
#
# PROBLEM: Play RECURSIVE Combat with card deck. Get score for winner.

deckfile="../data/day22_input.txt"
#deckfile="../data/day22_test.txt"

debug=True

################################################################################
# Every day the same....
def get_decks(deckfile) :
    deck1=[]
    deck2=[]
    readingdeck2=False
    with open(deckfile,"r") as df:
        for l in df:
            if "Player 2:" in l:
                readingdeck2=True
                continue
            try:
                v=int(l.strip())
                if readingdeck2 :
                    deck2.append(v)
                else :
                    deck1.append(v)
            except ValueError:
                continue
    return deck1,deck2

################################################################################
#These lists can be converted to a single string for ease of comparison later.
def save_state(deck1,deck2) :
    state="PA"
    for h in deck1 :
        state += str(h)
    state += "PB"
    for h in deck2 :
        state += str(h)
    return state

################################################################################
# This looks like it could be an expensive operation....
# (especially as the hand history needs to grow over time.)
# DEFINITION: State is duplicate if BOTH hands have been seen before IN THE SAME ORDER.
#(This is easier to check as a string.)
def is_duplicate_state(thisState,stateHistory) :
    for his in stateHistory :
        if thisState == stateHistory[his] :
            return True
    return False

################################################################################
def play_combat(deck1,deck2,depth) :
    if debug : print(f"BEGIN Game at depth {depth}.")
    turnhistory={}
    round=0
    while len(deck1)>0 and len(deck2)>0 :
        round+=1
        #Save turn history.
        turnstate = save_state(deck1,deck2)
        if not is_duplicate_state(turnstate,turnhistory) :
            turnhistory[round]=turnstate
        else :
            #In the event of a duplicate, rule states player 1 wins instantly
            if debug : print(f"DUPLICATE STATE AFTER {round} ROUNDS - ABORT WITH P1 WINNER")
            return True,deck1

        card1=deck1.pop(0)
        card2=deck2.pop(0)
        if debug :
            print(f"{round:4}: P1={deck1},P2={deck2}",end=",")
            print(f"P1={card1:3}, P2={card2:3}",end=":")
        #Do we need to recurse?
        if (len(deck1) >= card1) and (len(deck2) >= card2 ):
            if debug : print("RECURSING:")
            p1won,deck=play_combat(deck1[0:card1],deck2[0:card2],depth+1)
            #YES.
        else :
            #NO recursion, winner has the highest hand.
            p1won = (card1>card2)

        #Handle the win
        if p1won :
            #Player 1 won
            if debug : print("\t->P1")
            deck1.append(card1)
            deck1.append(card2)
        else :
            #Player 2 won
            if debug : print("\t->P2")
            deck2.append(card2)
            deck2.append(card1)

    #Determine who won and whose deck to return
    if debug : print(f"END OF GAME at depth {depth} after {round} rounds")
    if len(deck1)>0 :
        return True, deck1  #Player 1 won
    else :
        return False, deck2 #Player 2 won

################################################################################
################################################################################
################################################################################
if __name__ == '__main__' :
    deck1,deck2 = get_decks(deckfile)
    print("P1 starts with: ", deck1)
    print("P2 starts with: ", deck2)

    p1won,winningdeck = play_combat(deck1,deck2,1)

    #Post=game scoring.
    invertDeck=winningdeck[::-1]
    if p1won :
        print("Player 1 won")
    else :
        print("Player 2 won")

    score=0
    print(score)
    for i in range(len(invertDeck)) :
        print(f"+ {invertDeck[i]:2} * {i+1:2}")
        score += (i+1) * invertDeck[i]

    print("Final score was: ", score)
