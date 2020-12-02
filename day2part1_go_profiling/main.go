package main

/*
 problem spec:
     given a file containing a list of policies and passwords, find the number
     of passwords compliant with the policy.
     Input format:
        <num1>-<num2> <char>: <password>
     Policy:
        Compliant if <char> appears AT LEAST <num1> AND NO MORE THAN <num2>
        times in <password>
*/

import(
  "os"
  "log"
  "bufio"
  "strconv"
  "strings"
)

// struct to hold password policy data
type PassPolicy struct {
  n1 int
  n2 int
  c  string //maybe byte or rune?
  password string
}

// parser for input lines matching the spec above
func GetPassPolicyFromString(line string) PassPolicy {
   var aPassPolicy PassPolicy
   var polPass = strings.Split(line,": ")
   var polP1 = strings.Split(polPass[0]," ")
   var rang = strings.Split(polP1[0],"-")
   aPassPolicy.n1, _ = strconv.Atoi(rang[0])
   aPassPolicy.n2, _ = strconv.Atoi(rang[1])
   aPassPolicy.c = polP1[1]
   aPassPolicy.password = polPass[1]

   return aPassPolicy
}

//Count the number of times char "needle" appears in string "haystack"
func countOccurrences(needle,haystack string) int {
  var cCount int
  cCount = strings.Count(haystack,needle)
  return cCount
}


func day2part1() int {

  file,err := os.Open("../day2_input.txt")
  if err != nil {
    log.Fatal(err)
  }
  defer file.Close()

  passlist := []PassPolicy{}
  scanner := bufio.NewScanner(file)
  for scanner.Scan() {
    polLine := scanner.Text()
    passPol := GetPassPolicyFromString(polLine)
    passlist = append(passlist,passPol)
  }

  if err := scanner.Err(); err != nil {
    log.Fatal(err)
  }

  // AND NOW TO TACKLE THE ACTUAL PROBLEM......
  compliant := 0
  noncompliant := 0
  for _,pp := range passlist {
    numOccurrences := countOccurrences(pp.c,pp.password)
    if(numOccurrences >= pp.n1 && numOccurrences <= pp.n2) {
      compliant += 1
    } else {
      noncompliant += 1
    }
  }


  return compliant

}
