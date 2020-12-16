#!/usr/bin/python3
#
# My working for day 16, part 1
#
# PROBLEM:
#    Given input of a series of numbers with each line representing the
#    numbers on a ticket, but with the field-order unspecified and variant
#
#   And a separate set of "rules" dictating the values a given field can have
#
#   PART1: Determine which of the input tickets *cannot* be valid given the
#          various rules.
#
#   NOTES: In a break from previous days, the input is in 3 separate formats,
#          so I've decided to hard-code the definitions and just leave the
#          actual tickets as input data.
#
import sys

#Rules are expressed as a name, and a list of acceptable ranges for that field
rules = {
    'departure_location' : [[40,261],[279,955]],
    'departure_station'  : [[33,375],[394,963]],
    'departure_platform' : [[39,863],[877,970]],
    'departure_track'    : [[30,237],[256,955]],
    'departure_date'     : [[47,731],[741,950]],
    'departure_time'     : [[38,301],[317,954]],
    'arrival_location'   : [[26,598],[623,969]],
    'arrival_station'    : [[50,835],[854,971]],
    'arrival_track'      : [[36,672],[685,967]],
    'class'              : [[34,217],[236,974]],
    'duration'           : [[29,469],[483,970]],
    'price'              : [[45,111],[120,965]],
    'route'              : [[32,751],[760,954]],
    'row'                : [[25,321],[339,954]],
    'seat'               : [[38,423],[438,958]],
    'train'              : [[45,798],[813,954]],
    'type'               : [[40,487],[503,954]],
    'wagon'              : [[46,916],[938,949]],
    'zone'               : [[25,160],[184,957]] }

my_ticket = [73,59,83,127,137,151,71,139,67,53,89,79,61,109,131,103,149,97,107,101]

#Nearby tickets needs importing:
nearby_tickets=[]
ticketfile="../data/day16_input.txt"
with open(ticketfile,"r") as tf:
    foundNearbyTickets=False
    for l in tf:
        if not foundNearbyTickets and l.strip() == "nearby tickets:" :
            foundNearbyTickets=True
        elif foundNearbyTickets :
            fields=l.split(",")
            tick = []
            for f in fields:
                tick.append(int(f))
            nearby_tickets.append(tick)

print("Read {} nearby tickets from {}".format(len(nearby_tickets),ticketfile))
print(nearby_tickets[0])
print("...")
print(nearby_tickets[len(nearby_tickets)-1])

################################################################################
#Validation.....
validCount=0
invalidCount=0
invalidSum=0
for ticket in nearby_tickets :
    tickIsValid = True
    for fld in ticket :
        ruleMatch = False
        for rule in rules.keys() :
            for range in rules[rule] :
                print(f"Test {fld} against {rule}:{range}",end=":")
                if fld >= range[0] and fld <= range[1] :
                    ruleMatch = True
                    print(" OK")
                    break
            if ruleMatch :
                break
        if not ruleMatch :
            print(f"{fld} DOES NOT MATCH ANY RULE")
            tickIsValid = False
            invalidSum += fld
            break
    if tickIsValid :
        validCount +=1
    else :
        invalidCount +=1

print(f"{validCount} valid tickets; {invalidCount} invalid tickets")
print(f"Ticket Error Rate: {invalidSum}")
