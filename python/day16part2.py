#!/usr/bin/python3
#
# My working for day 16, part 2
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
#   PART2: Given that each ticket's scanned fields are in the same order,
#          determine which field is which from the rules for all valid tickets.
#
#   NOTES: In a break from previous days, the input is in 3 separate formats,
#          so I've decided to hard-code the definitions and just leave the
#          actual tickets as input data.
#
import sys

print("-"*25," Preamble (Data Read)  ", "-"*25)
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
    'arrival_platform'   : [[44,535],[549,958]],
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
#Validation..... and field tagging
validCount=0
invalidCount=0
invalidSum=0

#An "input" set of field tags by rule
ruleMatchingFields={}
for rule in rules :
    ruleMatchingFields[rule] = {}

#Phase 2 demands we analyse by field(column) but only if the whole ticket is valid
valid_tickets = []
for ticket in nearby_tickets :
    tickIsValid = True # All fields must match AT LEAST ONE rule to be valid.
    fldMatchesRule = {}
    i=0
    while i < len(ticket) :
        fldMatchesRule[i] = []
        fld=ticket[i]
        ruleMatch = False
        for rule in rules :
            for range in rules[rule] :
                if fld >= range[0] and fld <= range[1] :
                    ruleMatch = True
                    fldMatchesRule[i].append(rule)
        i+=1
        if not ruleMatch :
            tickIsValid = False
            invalidSum += fld
            break

    if tickIsValid :
        validCount +=1
        valid_tickets.append(ticket)
        #Update the global rules
        for i in fldMatchesRule :
            for r in fldMatchesRule[i] :
                if i not in ruleMatchingFields[r] :
                    ruleMatchingFields[r].update({i: [fld]})
                else :
                    ruleMatchingFields[r][i].append(fld)
    else :
        invalidCount +=1
print("-"*25," Nearby Ticket Analysis ", "-"*25)
print(f"{validCount} valid tickets; {invalidCount} invalid tickets")
print(f"Ticket Error Rate (your Part1 Answer, sir): {invalidSum}")

##############################################################################
# END OF (AUGMENTED) PART ONE. PART TWO SOLUTION FOLLOWS:
##############################################################################

#Invert ticket row/columns so we can search rule validity by column:
fldValues={}
for ticket in valid_tickets :
    i = 0
    while i < len(ticket) :
        if i not in fldValues :
            fldValues[i] = [ticket[i]]
        else :
            fldValues[i].append(ticket[i])
        i+=1

#Now search across fields looking for rule validity:
fld_cand_rules = {}
for fld in fldValues :
    for rule in rules :
        fld_matches_rule = True
        for v in fldValues[fld] :
            val_matches_range = False
            for r in rules[rule] :
                if v >= r[0] and v <= r[1] :
                    val_matches_range = True
            if not val_matches_range :
                fld_matches_rule = False
                break
        if fld_matches_rule :
            if fld not in fld_cand_rules :
                fld_cand_rules[fld] = {rule}
            else :
                fld_cand_rules[fld].add(rule)

print("-"*25," Field<->Rule Deduction  ", "-"*25)
#We now need to iteratively solve by reduction.
#(I only know this works because I peeked at the output above. This is not a
# general solution to the problem and has a non-terminating error condition)
FieldRuleMappings={}
inPlayFields = list(fld_cand_rules.keys())
inPlayRules = list(rules.keys())
while len(inPlayFields)>0 :
    print("UNSOLVED:",len(inPlayFields))
    unsolvedFields = []
    for f in inPlayFields :
        if len(fld_cand_rules[f]) == 1 :
            #BINGO. This field only has 1 valid rule mapping.
            rule=fld_cand_rules[f].pop()
            FieldRuleMappings[f]=rule
            inPlayRules.remove(rule)
            print(f"\tSOLVED: {f} = {rule}")
            #ITERATE and remove this from all other fld_cand_rules:
            for f in fld_cand_rules :
                fld_cand_rules[f].discard(rule)
        else :
            unsolvedFields.append(f)
    #non-termination check - we should have reduced the unsolved fields
    if len(unsolvedFields) == len(inPlayFields) :
        print("!!!!!! ERROR NO SOLVED FIELDS")
        print("Something's gone wrong with the iterative solver algo. Aborting")
        exit(1)
    else :
        inPlayFields = unsolvedFields


print("-"*25," Field Mappings ", "-"*25)
for f in sorted(FieldRuleMappings.keys()) :
    print(f"{f:2} : {FieldRuleMappings[f]}")

####################################################################
#And now the finale. Per the rules, find the product of the 6 fields
#starting "departure" in my input ticket:
print("-"*25," My Ticket Analysis ", "-"*25)
product=1
i=0
while i < len(my_ticket) :
    if FieldRuleMappings[i].startswith("departure") :
        print(f"Field {i} is {FieldRuleMappings[i]} value {my_ticket[i]}")
        product *= my_ticket[i]
    i+=1

print(f"Product of Departure fields (your Part2 answer, sir): {product}")
