#!/usr/bin/python3
#
# My working for Day 5, Part 2
#
# PROBLEM SPEC:
#      Airline Seating encoded as binary partition in format {7}:{3}
#          F=Front, B=Back, L=Left, R=Right.
#      Rows go from 0-127
#      Columns go from 0-7
#      Seat ID also expressable as (row*8)+column (numbered from front/left)
#
#      Given that "some of the seats at the front and back of the plane don't"
#      exist" but that "the seats with IDs adjacent to yours - +1, -1 - DO exist"
#      find your seat (the missing seat id)
import sys

seatcodes=[]
with open("day5_input.txt", "r") as enc:
    for l in enc:
        try:
            rowenc = l[0:7]
            colenc = l[7:10]
            seatcodes.append([rowenc,colenc])
        except IndexError:
            print("can't start decoding line |{0}|".format(l))

maxSid = 0
sidlist = []
for sc in seatcodes:
    #Decode the row
    d=64
    row=0
    for c in sc[0] :
        if c == "F" :
            row = row
        else :
            row = row + d
        d = d/2
    row=int(row)
    #Decode the Column
    d=4
    col=0
    for c in sc[1] :
        if c == "L" :
            col = col
        else :
            col = col + d
        d = d/2
    col=int(col)

    #Calculate the Seat ID from this row,col pair and see if it's the max
    sid = row*8 + col
    sidlist.append(sid)
    if sid > maxSid :
        maxSid = sid

print("Max SID found: {0}".format(maxSid))

#PART 2 starts here: 
sidlist = sorted(sidlist)
candSID=[]
for i in range(len(sidlist)) :
    #Skip first and last elements of list
    if i==0 or i==(len(sidlist)-1) :
        continue
    #method: values either side of ours should be the same as our value +/- 1
    #if not, we have a candidate. This algorithm SHOULD find 2 SIDs, and the
    #missing SID - our seat - is the one "inbetween" those two values
    print(i)
    if sidlist[i-1] != sidlist[i]-1 or sidlist[i+1] != sidlist[i]+1 :
        candSID.append(sidlist[i])

print(candSID)
