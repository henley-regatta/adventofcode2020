package main
/*
# PROBLEM: Play Crab Cups with some made-up complexities -
#          a million cups over ten million rounds.
#
#   Given an input list of INTs, these represent a "circle" of cups clockwise
#   from the first in the list (modulo arithmetic). The game rules are:
#      * First cup becomes CURRENT.
#      * Cups 2,3,4 are REMOVED from list.
#      * DESTINATION cup selected as <Current LABEL>-1
#            * If DESTINATION was in the REMOVED list, select <Current Label>-2
#              (repeat until matched. Wrap-around as required)
#      * <REMOVED> are then placed immediately *clockwise* of DESTINATION in
#        their original order
#      * CURRENT is selected as next in the list.

(Adapted from my Python answer, as an attempt to do large maps in Go)

*/
import (
  "fmt"
  //"log"
  "time"
)

//------------------------------------------------------------------------------
func build_cup_linkedlist(initCups []int, totalLength int)  map[int]int {
    cuplist := make(map[int]int)
    //Scheme is: Build the initial list from the string of numbers passed in,
    //expand to the length requested linking n-1->n except for the last which
    //links to the first.
    cupZero:=initCups[0]
    cMin:=99999999
    cMax:=0
    prevC:=0
    for i,dv := range initCups {
      //Bookkeeping min/max
      if(dv<cMin) { cMin=dv}
      if(dv>cMax) { cMax=dv}
      if i==0 {
        cupZero = dv
        prevC=dv
      //General case - cup n-1 links to cup n
      } else {
        cuplist[prevC]=dv
        prevC=dv
      }
    }
    defLen:=len(cuplist)+1
    //And will run to make up <totalLength> entries:
    for i := defLen+1; i<=totalLength; i++ {
      cuplist[prevC]=i
      prevC=i
    }
    //link final element back to cupZero
    cuplist[len(cuplist)+1] = cupZero

    return cuplist
}
//------------------------------------------------------------------------------
func sanity_check_linked_list(ll map[int]int, fromStart int) bool {
  //List is valid if LAST element links back to FIRST element, and following
  //the chain goes through EVERY element in the list exactly once.
  hopCount:=1
  expectedHops:=len(ll)
  cHop := ll[fromStart]
  for cHop != fromStart && hopCount<=expectedHops {
    nHop := ll[cHop]
    //fmt.Printf("hop %d:  %d -> %d\n", hopCount,cHop,nHop)
    hopCount++
    if nHop == fromStart && hopCount!=expectedHops {
      fmt.Printf("Loop linked to start (%d) after only %d of %d expected hops\n",
        fromStart,
        hopCount,
        expectedHops)
      return false //Linked to start too soon
    }
    cHop = nHop
  }

  if cHop == fromStart && expectedHops==hopCount {
      return true
  }
  fmt.Printf("Loop didn't link back to start (%d) after expected %d hops, only %d taken\n",
      fromStart,
      expectedHops,
      hopCount)
  return false
}

//------------------------------------------------------------------------------
// MAPS are always pass-by-reference so there's no funky pointer arithmetic
//      required. We always end up modifying the global value. A benefit, in this
//      case...
func crab_cups_round(cuplist map[int]int, currentCup,cMin,cMax int) int {
  var removed [3]int
  removed[0]=cuplist[currentCup]
  removed[1]=cuplist[removed[0]]
  removed[2]=cuplist[removed[1]]
  ptrNext := cuplist[removed[2]]
  //point the current entry "beyond" the removed cups:
  cuplist[currentCup] = ptrNext

  //Apply the crab-cups rule: "target" is current-1 with wrap-around if needed
  foundTarget:=false
  destCup:=currentCup
  for !foundTarget {
    if destCup>cMin {
      destCup = destCup-1
    } else {
      destCup = cMax
    }
    //Check this value hasn't been removed
    if removed[0]!=destCup && removed[1]!=destCup && removed[2]!=destCup {
      foundTarget=true
    }
  }

  //Update the linkage by re-inserting the removed AFTER target cup.
  orgPtr := cuplist[destCup]
  cuplist[destCup] = removed[0]
  cuplist[removed[0]] = removed[1]
  cuplist[removed[1]] = removed[2]
  cuplist[removed[2]] = orgPtr

  //And finish by returning whatever is now after the current cup
  return cuplist[currentCup]

}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
func main() {
  //Live data:
  initCups := []int{4,1,8,9,7,6,2,3,5}
  //(Actual answer: 563362809504)
  //Test data:
  //(Expected result: 1 next to 934001,159792. Answer: 149245887792)
  //initCups := []int{3,8,9,1,2,5,4,6,7}

  preInit := time.Now()
//  cuplist := build_cup_linkedlist(initCups,1000000)
  cuplist := build_cup_linkedlist(initCups,1000000)
  postInit := time.Now()
  initElapsed := postInit.Sub(preInit)
  fmt.Printf("Initialising the Cups List to %7d entries took %3.2f seconds\n",
             len(cuplist),
             (initElapsed.Seconds() * 1e6) /1e6)
  preCheck := time.Now()
  isValidChain := sanity_check_linked_list(cuplist,initCups[0])
  postCheck := time.Now()
  chkElapsed := postCheck.Sub(preCheck)
  fmt.Printf("Sanity-checking initial list took %3.2f seconds and isvalid=%t\n",
    (chkElapsed.Seconds() * 1e6 ) / 1e6,
    isValidChain)
  //re-calculate the min and max values in the cuplist.
  cupMin:=9999999999999
  cupMax:=0
  for _,v := range cuplist {
    if v>cupMax { cupMax=v}
    if v<cupMin { cupMin=v}
  }

  //Now play the game the proscribed number of turns
  maxRounds := 10000000
  current:=initCups[0]
  tStart := time.Now()
  for i := 0; i<maxRounds; i++ {
    current = crab_cups_round(cuplist,current,cupMin,cupMax)
  }
  tEnd := time.Now()
  tDiff := tEnd.Sub(tStart)
  tRate := int64(maxRounds*1000000) / tDiff.Microseconds()
  validpostExecution:=sanity_check_linked_list(cuplist,initCups[0])
  fmt.Printf("%d rounds of Crab Cups took %3.2f or %d rounds/sec and the result is valid: %t\n",
    maxRounds,
    (tDiff.Seconds() * 1e6)/1e6,
    tRate,
    validpostExecution)

  iNext:=cuplist[1]
  iNextPlus:=cuplist[iNext]
  fmt.Printf("The numbers after 1 are %d and %d\n",iNext,iNextPlus)

  partTwoAnswer := iNext * iNextPlus
  fmt.Printf("The Part Two answer is therefore: %d\n",partTwoAnswer)


}
