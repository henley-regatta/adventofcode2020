#!/usr/bin/python3
# My working for day 4 part 1
#
# PROBLEM:
#       Given an input file containing "passport" data, determine how many
#       records are valid.
#       Records are delimited by a blank line.
#       Fields are delimited by space or newline.
#       Fields are of the form <key>:<value>
#       Valid records have 7 or 8 fields:
#         byr,iyr,eyr,hgt,hcl,ecl,pid,cid.
#       (cid is optional; records without it are valid.)
#       Records missing any field with the exception of cid are invalid.
import sys

#Struct holding the passport records.
precords = []

#Fields that should exist in the record
frec = [ 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']

def reportMissingFields(fldlist,record) :
    missingflds = {}
    for f in fldlist :
        missingflds[f] = True

    for fld in record :
        if missingflds[fld] :
            missingflds.pop(fld)

    return missingflds

#Actually, reading the file is most of the processing here....
#(but since there will be a part 2, do it properly)
with open("day4_input.txt","r") as f:
    trec = {}
    for l in f:
        fld = l.strip('\n').split(' ')
        if len(fld)>0 and len(fld[0])>0 :
            for t in fld:
                kvp=t.split(":")
                if len(kvp)==2 :
                    trec[kvp[0]] = kvp[1]
        elif len(trec)>0 :
            #emd of record, it's a blank line
            precords.append(trec)
            trec = {}
    #dump final record
    precords.append(trec)

totrec = len(precords)
validrec = 0
invalidrec = 0
missingcid = 0

for rec in precords:
    if len(rec) == 8 :
        validrec = validrec + 1
    elif len(rec)>6 :
        #get missing fields in record
        missingFlds = reportMissingFields(frec,rec)
        if 'cid' in missingFlds :
            missingcid = missingcid + 1
        if len(missingFlds) == 1 and 'cid' in missingFlds:
            validrec = validrec + 1
        else :
            invalidrec = invalidrec + 1
    else :
        invalidrec = invalidrec + 1

print("Of the {0} records, {1} were valid ({2} were missing cid)".format(totrec,validrec,missingcid))
print("(means that {0} were invalid; checkcount: {1})".format(invalidrec,validrec+invalidrec))
