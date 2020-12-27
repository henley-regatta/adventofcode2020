#!/usr/bin/python3
#
# My solution for Day 25 Part 1


#My puzzle input:
card_pubkey=14012298
door_pubkey=74241

#Sample puzzle input:
#card_pubkey=5764801
#door_pubkey=17807724

##############################################################################
def transform_subject(subject,loop) :
    v=1
    for i in range(loop) :
        v = v * subject
        v = v % 20201227
    return v

##############################################################################
#For (at least) performance reasons I need to cache the result of loop n-1
def find_secret_loops(input_pubkey) :
    tloop=0
    foundSecretLoop=False
    prev_transform=1
    while not foundSecretLoop :
        tloop+=1
        #Inner transform loop
        prev_transform = prev_transform * 7
        prev_transform = prev_transform % 20201227
        if prev_transform == input_pubkey :
            foundSecretLoop=True
    return tloop

##############################################################################
##############################################################################
##############################################################################
if __name__ == '__main__' :
    card_loops=find_secret_loops(card_pubkey)
    print(f"Card {card_pubkey} has {card_loops} as the secret loop number")
    door_loops=find_secret_loops(door_pubkey)
    print(f"Door {door_pubkey} has {door_loops} as the secret loop number")
    print(f"Calculated Card loops = {card_loops}, Door loops = {door_loops}")

    enc_key = transform_subject(door_pubkey,card_loops)
    #verify
    chk_key = transform_subject(card_pubkey,door_loops)
    if enc_key != chk_key :
        print(f"Something wrong with maths. {enc_key} != {chk_key}")
    else :
        print(f"The (part one) Secret Encryption key is: {enc_key}")
