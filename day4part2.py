#!/usr/bin/python3
# My working for day 4 part 2
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
#       Field validation should be performed:
#           byr - four digits, >=1920 && <=2002
#           iyr - four digits, >=2010 && <=2020
#           eyr - four digits, >=2020 && <=2030
#           hgt - number<in|cm>
#                 if cm:  >=150 && <=193
#                 if in:  >=59  && <=76
#           hcl - #[0-9|a-f]{6}
#           ecl - enum: [amb|blu|brn|gry|grn|hzl|oth]
#           pid - [0-9]{9}
import sys
import re

#U KNOW a toy problem is bad when it requires the addition of a debug harness
debug=False

#Struct holding the passport records.
precords = []

#Fields that should exist in the record
frec = [ 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']

#I GIVE IN. It's a regular expression job.
hclPat = re.compile('^\#[0-9|a-f]{6}$')

#############################################################################
def validateRecord(record) :

    missingFlds = reportMissingFields(frec,record)
    #Basic check - should have all fields defined (with possible exception of 'cid')
    if len(missingFlds) > 1 or (len(missingFlds) == 1 and 'cid'  not in missingFlds) :
        return "fldCount"

    #FIELD VALIDATION TIME:
    for fld in record :
        if fld == 'byr' :
            if not fldWithinRange(record[fld], 1920, 2002) :
                return "byr"
        if fld == 'iyr' :
            if not fldWithinRange(record[fld], 2010, 2020) :
                return "iyr"
        if fld == 'eyr' :
            if not fldWithinRange(record[fld], 2020, 2030) :
                return "eyr"
        if fld == 'hgt' :
            #There's a shortcut available per the spec:
            hgt=record[fld]
            if len(hgt) == 4 and hgt[2:4] == "in": #Inches
                try:
                    h=int(hgt[0:2])
                    if h<59 or h>76 :
                        return "hgt"
                except ValueError:
                    return "hgt"
            elif len(hgt) == 5 and hgt[3:5] == "cm": #Centimeters
                try:
                    h=int(hgt[0:3])
                    if h<150 or h>193 :
                        return "hgt"
                except ValueError:
                    return "hgt"
            else :
                return "hgt"
        if fld == 'hcl' :
            if not re.search(hclPat,record[fld]) :
                return "hcl"
        if fld == 'ecl' :
            if record[fld] not in [ 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth' ] :
                return "ecl"
        if fld == 'pid' :
            try:
                pid=int(record[fld])
                if len(record[fld]) != 9 or pid < 0 or pid > 999999999 :
                    return "pid"
            except ValueError:
                return "pid"

    #If we got here we must have passed all checks.
    return "ok "

#############################################################################
def fldWithinRange(fld,minVal,maxVal) :
    try:
        fVal = int(fld)
    except ValueError:
        return False
    if fVal < minVal or fVal > maxVal :
        return False

    return True

#############################################################################
def reportMissingFields(fldlist,record) :
    missingflds = {}
    for f in fldlist :
        missingflds[f] = True

    for fld in record :
        if missingflds[fld] :
            missingflds.pop(fld)

    return missingflds

#############################################################################
#############################################################################
#############################################################################
#Actually, reading the file is most of the processing here....
#(but since there will be a part 2, do it properly)
#with open("d4p2test.txt","r") as f:
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


for rec in precords:
    failCode = validateRecord(rec)
    if failCode == "ok " :
        validrec = validrec + 1
    else :
        invalidrec = invalidrec + 1

    if debug :
        #This did my head in so much I dump output in CSV format so I can
        #analyse it in Google Sheets. Which is what caught my final validation
        #error - I'd removed a length check from pid.... HOURS LATER.
        print('"{0}"'.format(failCode),end=",")
        if "cid" not in rec :
            rec["cid"] = "N/A"
        for k,v in sorted(rec.items(), key=lambda x: x[0]) :
            print('"{0}"'.format(v), end=",")
        print('"END"')

print("Of the {0} records, {1} were valid".format(totrec,validrec))
print("(means that {0} were invalid; checkcount: {1})".format(invalidrec,validrec+invalidrec))
