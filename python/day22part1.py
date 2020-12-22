#!/usr/bin/python3
#
# My working for day 22 part 1.
#
# PROBLEM: Play Combat with card deck. Get score for winner.


deckfile="../data/day22_input.txt"
#deckfile="../data/day22_test.txt"

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

print("Deck 1:", deck1)
print("Deck 2:", deck2)

round=0
while len(deck1)>0 and len(deck2)>0 :
    round+=1
    print(f"{round:4}: P1={deck1},P2={deck2}",end=",")
    card1=deck1.pop(0)
    card2=deck2.pop(0)
    print(f"P1={card1:3}, P2={card2:3}",end=":")
    if card1 > card2 :
        #Player 1 won
        print("\t->P1")
        deck1.append(card1)
        deck1.append(card2)
    else :
        #Player 2 won
        print("\t->P2")
        deck2.append(card2)
        deck2.append(card1)

invertDeck=[]
if len(deck1)==0 :
    print("Player 2 won",end=" ")
    invertDeck=deck2[::-1]
else :
    print("Player 1 won",end=" ")
    invertDeck=deck1[::-1]
print(f"after {round} rounds")

score=0
print(score)
for i in range(len(invertDeck)) :
    print(f"+ {invertDeck[i]:2} * {i+1:2}")
    score += (i+1) * invertDeck[i]

print("Final score was: ", score)
