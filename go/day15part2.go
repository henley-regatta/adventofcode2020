package main
/*
# PROBLEM:
#    The "Elf Game" has the following rules:
#       * There is a starting set of numbers
#       * At each turn AFTER the initial set of numbers
#         has been spoken, the player must either state
#         0 - the previous number has never been seen before
#         n - The previous number came up n turns ago.
#         (strictly speaking the difference between the last 2
#          utterences.)
#
#  Given an input starting set, determine the 30000000th  number spoken.
*/

import(
  "fmt"
  "log"
  "time"
)

/*
------------------------------------------------------------------------------
Initialise the game by creating the "last seen" map
*/
func startElfGame(startNumbers []int) (int, map[int]int, map[int]int) {
  lastMap := map[int]int{}
  prevMap := map[int]int{}
  turn := 1
  for i := range(startNumbers) {
    lastMap[startNumbers[i]] = turn
    prevMap[startNumbers[i]] = 0
    turn++
  }
  return turn,lastMap,prevMap
}


/*
------------------------------------------------------------------------------
*/
func playElfGame(startNumbers []int, iterations int) int {
  i,lastMap,prevMap := startElfGame(startNumbers)
  fmt.Printf("Game initialised as: %#v, %#v and next turn %d\n",lastMap,prevMap,i)
  lastSpoken := startNumbers[len(startNumbers)-1]
  for i <= iterations {
    nextSpoken := 0 //A handy default
    //Game Rules:
    // Examine the answer from the last iteration. Has it been spoken before?
    lastSeen,lFound := lastMap[lastSpoken]
    prevSeen,pFound := prevMap[lastSpoken]
    if (lFound && !pFound) || (!lFound && pFound) { //Catch a data-error
      log.Fatal("Data error - no match between last/previous found maps for v=", lastSpoken)
    } else if !lFound && !pFound {   //We've never seen this before, answer is Zero (as above)
      lastMap[lastSpoken] = i-1 //Initialise history for this
      prevMap[lastSpoken] = 0
    } else {
      if prevSeen == 0 {  //We've seen this once before. Special case, was it on last turn?
        if lastSeen == i-1 { //Yes - answer Zero
          nextSpoken = 0
        } else { //No - Answer with diff
          nextSpoken = (i-1) - lastSeen
        }
      } else { //We've seen the number X times before...
        nextSpoken = lastSeen - prevSeen
      }
      //Update stored values if we ever saw this before:
      t:=lastMap[nextSpoken]
      prevMap[nextSpoken] = t
      lastMap[nextSpoken] = i
    }
    //Get ready for the next turn...
    i++
    lastSpoken = nextSpoken
  }
  return lastSpoken
}

/*
------------------------------------------------------------------------------
*/
func runHarness(startNumbers []int, iterations int) int64 {

  start := time.Now()
  answer := playElfGame(startNumbers,iterations)
  t := time.Now()
  elapsed := t.Sub(start)
  turnRate := int64(iterations*1000000) / elapsed.Microseconds()

  fmt.Printf("Answer after %-8d iterations: %-5d (took %.6f seconds; %-8d turns/second)\n",
    iterations,
    answer,
    (elapsed.Seconds() * 1e6) /1e6,
    turnRate,
  )
  return turnRate
}

/*
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
*/
func main() {

  //Test Data i=2020,a=438. i=30000000,a=18
  //startNumbers := []int{3,2,1}
  //Test Data i=2020, a=436. i=30000000, a=175594
  //startNumbers := []int{ 0,3,6 }
  //Actual puzzle input:
  startNumbers := []int{ 0,5,4,1,10,14,7 }

  turnRate := runHarness(startNumbers,2020)
  fmt.Printf("Predicted execution time for 202020 turns: %.4f seconds\n",
    float64(202020) / float64(turnRate),
  )

  turnRate = runHarness(startNumbers,202020)
  fmt.Printf("Predicted execution time for 30000000 turns: %.4f seconds\n",
    float64(30000000) / float64(turnRate),
  )

  turnRate = runHarness(startNumbers,30000000)




}
