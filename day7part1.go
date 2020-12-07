package main
/*
# PROBLEM SPEC:
#    Given a list of input rules of the form:
#     <colour> bags contain <x> <colour> bags{, <y> <colour> bags}
#        OR
#     <colour> bags contain no other
#
#    ...Determine the number of <colour> bags that can contain at least one
#       Shiny Gold bag (either directly or indirectly)
*/
import (
  "fmt"
  "os"
  "bufio"
  "log"
  "strings"
  "strconv"
  "regexp"
)

type SubBagDef struct {
  colour string
  numbags int
}

type BagRule struct {
  colour string
  subbags []SubBagDef
}

func parseInputRulesFile(filename string) []BagRule {
  bagrules := []BagRule{}
  firstRE := regexp.MustCompile(`(?P<colour>.+) bags contain (?P<numbags>[0-9]+) (?P<subcolour>.+) bag`)
  noSubRE := regexp.MustCompile(`(?P<colour>.+) bags contain no other`)
  subRE   := regexp.MustCompile(`\D*(?P<numbags>[0-9]+) (?P<subcolour>.+) bag`)
  fh,err := os.Open(filename)
  if err != nil {
    log.Fatal(err)
  }
  defer fh.Close()
  s := bufio.NewScanner(fh)
  for s.Scan() {
    l := s.Text()
    //first level split: by comma. Check first element matches expectation
    elem := strings.Split(l,", ")
    //get match
    complexMatch := firstRE.FindAllStringSubmatch(elem[0],-1)
    if complexMatch == nil {
      terminalMatch := noSubRE.FindAllStringSubmatch(elem[0],-1)
      if terminalMatch == nil {
        log.Output(0,"SRC LINE INVALID: "+l)
      } else {
        bagrules = append(bagrules, BagRule{ colour: terminalMatch[0][1]})
      }
    } else {
      numBags,_ := strconv.Atoi(complexMatch[0][2])
      firstSubBag := SubBagDef{ colour: complexMatch[0][3], numbags: numBags}
      br := BagRule{ colour: complexMatch[0][1], subbags: []SubBagDef{firstSubBag}}
      for i:= 1; i<len(elem); i++ {
        sbr := subRE.FindAllStringSubmatch(elem[i],-1)
        if sbr != nil {
          sbc,_ := strconv.Atoi(sbr[0][1])
          sbd := SubBagDef{ colour: sbr[0][2], numbags: sbc}
          br.subbags = append(br.subbags,sbd)
        } else {
          log.Output(1, "SUB CLAUSE NO MATCH: "+elem[i])
        }
      }
      bagrules = append(bagrules,br)
    }
  }
  return bagrules
}

// ---------------------------------------------------------------------------
func findIsContainedBy(tgtColour string, bagrules []BagRule) []string {
  var isContainedBy []string
  for i := range bagrules {
    for j := range bagrules[i].subbags {
      if bagrules[i].subbags[j].colour == tgtColour {
        isContainedBy = append(isContainedBy, bagrules[i].colour)
      }
    }
  }
  return isContainedBy
}

// ---------------------------------------------------------------------------
func isInList(tgtColour string, listOfColours []string) bool {
  for i := range listOfColours {
    if listOfColours[i] == tgtColour {
      return true
    }
  }
  return false
}

// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------

func main() {
  bagrules := parseInputRulesFile("day7_input.txt")
  //bagrules := parseInputRulesFile("d7_test.txt")
  //fmt.Printf("%#v\n",bagrules)
  fmt.Println("Parsed " + strconv.Itoa(len(bagrules)) + " rules from input file")

  tgtColour := "shiny gold"
  alreadySeen := findIsContainedBy(tgtColour, bagrules)

  fmt.Println(tgtColour + " is directly contained by " + strconv.Itoa(len(alreadySeen)) + " bags: ")
  //fmt.Printf("%#v\n",alreadySeen)

  totCount := len(alreadySeen)
  //recurse and find sub-counts discarding those we've already seen
  searchList := alreadySeen
  for len(searchList)>0 {
    //Pop first element from the search list:
    inCol := searchList[0]
    searchList = searchList[1:]
    //find what colours contain this
    subContainsList := findIsContainedBy(inCol,bagrules)
    //If it's not already on our list, add it:
    for fCol := range subContainsList {
        if ! isInList(subContainsList[fCol],alreadySeen) {
          totCount += 1
          //stop double-counts
          alreadySeen = append(alreadySeen,subContainsList[fCol])
          //but search found colour for further indirection:
          searchList = append(searchList,subContainsList[fCol])
        }
    }
  }

  fmt.Println(tgtColour + " is directly and indirectly contained by " + strconv.Itoa(totCount) + " bag colours")
}
