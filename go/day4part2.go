package main

/*
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
*/

import(
  "fmt"
  "os"
  "log"
  "bufio"
  "strconv"
  "strings"
)

type PassportRecord struct {
  pid string
  cid int
  byr int
  iyr int
  eyr int
  hgt int
  hgttype string
  hcl string
  ecl string
  valid bool
}

/*
----------------------------------------------------------------------------------
----------------------------------------------------------------------------------
----------------------------------------------------------------------------------
*/

//--------------------------------------------------------------------------------
//Parsing these records is painful enough that I want to make it multi-stage
func readFileIntoRecords(fname string) []string {
  file,err := os.Open(fname)
  if err != nil {
    log.Fatal(err)
  }
  defer file.Close()

  rec := ""
  var reclist []string

  sc := bufio.NewScanner(file)
  for sc.Scan() {
    l := sc.Text()
    if len(l) > 0 {
      rec = rec + " " + l
    } else {
      reclist = append(reclist,rec)
      rec = ""
    }
  }
  return append(reclist,rec)
}


//--------------------------------------------------------------------------------
//Parsing these records is painful enough that I want to make it multi-stage
func parseRecordIntoFieldPairs(record string) [][]string {
  //split in record by space and process that way
 var outRecord [][]string
 flds := strings.Fields(record)
 for _,fld := range flds {
   kvp := strings.Split(fld,":")
   outRecord = append(outRecord,kvp)
 }
 return outRecord
}

//--------------------------------------------------------------------------------
// helper for the numneric values with accepted ranges
func getAgeRange(yeartext string, vmin,vmax int) int {
  val,err := strconv.Atoi(yeartext)
  if err != nil || val < vmin || val > vmax {
    return 0
  } else {
    return val
  }
}


//--------------------------------------------------------------------------------
//The theory goes that if I make this robust enough it'll give me the answer
//just by returning a valid record
func parseKVPRecordIntoPassportRecord(kvp_rec [][]string) PassportRecord {
  var prec PassportRecord
  prec.valid = true
  if len(kvp_rec) < 7 { prec.valid = false; return prec}
  for _,kvp := range kvp_rec {
    switch kvp[0] {
      case "eyr" : {
        prec.eyr = getAgeRange(kvp[1], 2020, 2030)
        if prec.eyr == 0 { prec.valid = false}
      }
      case "iyr" : {
        prec.iyr = getAgeRange(kvp[1], 2010, 2020)
        if prec.iyr == 0 { prec.valid = false }
      }
      case "byr" : {
        prec.byr = getAgeRange(kvp[1], 1920, 2002)
        if prec.byr == 0 { prec.valid = false }
      }
      case "cid" : {
        prec.cid = getAgeRange(kvp[1],0,999999999) //no test here any value is valid
      }
      case "pid" : {
        tpid := getAgeRange(kvp[1],0,999999999)
        if tpid > 0 && len(kvp[1]) == 9 {
          prec.pid = kvp[1]
        } else {
          prec.pid = "N/A"
          prec.valid = false
        }
      }
      case "hcl" : {
        if len(kvp[1]) == 7 && kvp[1][0] == '#'  {
          _,err := strconv.ParseInt(kvp[1][1:6],16,24)
          if err == nil {
            prec.hcl = kvp[1]
          } else {
            prec.hcl = "N/A"
            prec.valid = false
          }
        } else {
          prec.hcl = "N/A"
          prec.valid = false
        }
      }
      case "hgt" : {
        if len(kvp[1]) == 5 && kvp[1][3:5] == "cm" {
          prec.hgttype = kvp[1][3:5]
          h,err := strconv.Atoi(kvp[1][0:3])
          prec.hgt = h
          if err != nil || h < 150 || h > 193 {
            prec.valid = false
          }
        } else if len(kvp[1]) == 4 && kvp[1][2:4] == "in" {
          prec.hgttype = kvp[1][2:4]
          h,err := strconv.Atoi(kvp[1][0:2])
          prec.hgt = h
          if err != nil || h < 59 || h > 76 {
            prec.valid = false
          }
        } else {
          prec.hgt = 0
          prec.hgttype = "N/A"
          prec.valid = false
        }
      }
      case "ecl" : {
          switch kvp[1]  {
            case "amb", "blu", "brn", "gry", "grn", "hzl", "oth" : {
              prec.ecl = kvp[1]
            }
            default : {
              prec.ecl = "N/A"
              prec.valid = false
            }
          }
      }
      //any key without a match should result in:
      default : { prec.valid = false }
    }
  }

  //Sanity check that we've got non-default values for all required keys
  if prec.valid &&
     len(prec.pid)>0 && prec.pid != "N/A" &&
     prec.iyr > 0 &&
     prec.eyr > 0 &&
     prec.byr > 0 &&
     prec.hgt > 0 && (prec.hgttype == "in" || prec.hgttype == "cm") &&
     len(prec.ecl)>0 && prec.ecl != "N/A" &&
     len(prec.hcl)>0 && prec.hcl != "N/A"  {
    prec.valid = true
  } else {
    prec.valid = false
  }
  return prec
}
/*
----------------------------------------------------------------------------------
----------------------------------------------------------------------------------
----------------------------------------------------------------------------------
*/
func main() {

  prec_text := readFileIntoRecords("../data/day4_input.txt")
  var passport_records []PassportRecord
  for _,rec_text := range prec_text {
    kvp_rec := parseRecordIntoFieldPairs(rec_text)
    pass_rec := parseKVPRecordIntoPassportRecord(kvp_rec)
    if pass_rec.valid {
      passport_records = append(passport_records,pass_rec)
    }
  }

  fmt.Println("Read ", len(passport_records), " valid passport records from file.")

}
