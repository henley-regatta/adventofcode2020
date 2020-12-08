#!/usr/bin/python3
#
# My working for Day 5, Part 1
#
# PROBLEM SPEC:
#      Airline Seating encoded as binary partition in format {7}:{3}
#          F=Front, B=Back, L=Left, R=Right.
#      Rows go from 0-127
#      Columns go from 0-7
#      Seat ID also expressable as (row*8)+column (numbered from front/left)
#
#      Given a set of input Seating codes, what is the highest SeatID found?
import sys

seatcodes=[]
with open("../data/day5_input.txt", "r") as enc:
    for l in enc:
        try:
            rowenc = l[0:7]
            colenc = l[7:10]
            seatcodes.append([rowenc,colenc])
        except IndexError:
            print("can't start decoding line |{0}|".format(l))

maxSid = 0
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
    if sid > maxSid :
        maxSid = sid

    print("{0} -> ({1},{2}) -> {3}".format(sc,row,col,sid))

print("Max SID found: {0}".format(maxSid))
