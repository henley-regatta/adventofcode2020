package main
/*
#  PROBLEM
#    Given a range of "joltage adapters" having a defined output "joltage"
#    and with the characteristic that each can take an input of 1-3 "jolts"
#    lower than rated voltage, work out the range of joltage differences
#    between the wall (0 jolts) and your device (output = largest adapter
#    joltage + 3 ) when using all adapters.
#
#    Calculate the number of permutations of adapters that can be used
#    to bridge between input (0 Jolts) and Device (maxAdapter + 3 Jolts) joltage.
#
#    NOTE: Simple algorithms won't scale to the depth of input required. Which
#          is a shame.

The optimised solution algorithm I'm using here only works because the input
and rules permit it, specifically:
  * No two adapters have the same Joltage
  * Joltages always increment from wall to device
  * There are no "impassable jumps" in Joltage

...which means the algorithm can just calculate "tail" permutations once and
store them to prevent the need to re-calculate on later chains (as the "tails"
from a given point are always the same)

As a Go learning exercise, this is more about holding/modifying global structures
than anything else.
*/

import(
  "os"
  "log"
  "bufio"
  "strconv"
  "sort"
  "fmt"
)

//Because we need to access & modify this from within functions, it has to be
//declared in the global scope. Initialise with the "wall joltage" only.
var subPermCount = map[int]int{ 0 : 0}

/*
---------------------------------------------------------------------------------
*/
func readAdaptersFromFile(filename string) []int {
  var adapterlist []int
  fh,err := os.Open(filename)
  if err != nil {
    log.Fatal(err)
  }
  defer fh.Close()
  s := bufio.NewScanner(fh)
  for s.Scan() {
    l := s.Text()
    num, _ := strconv.Atoi(l)
    adapterlist = append(adapterlist,num)
  }

  return adapterlist
}

/*
---------------------------------------------------------------------------------
This is the guts of the solution. Calculate *AND STORE* a sub-permutations count
for parameter X by summing all possible sub-permutations. The *AND STORE* part
of the solution turns this from O(n^n) to O(2n) (by inspection-only)
*/
func calc_subpermutations_from_x(x int) int {
  if subPermCount[x] == 0 {
    //Needs calculating...
    //(range on a map returns the keys)
    for n := range subPermCount {
      if n<(x+1) || n>(x+3) {
        //n out of "next element" range, skip it.
        continue
      } else {
        //n is within the evaluation range, work out all sub-perms from it
        subPermCount[x] = subPermCount[x] + calc_subpermutations_from_x(n)
      }
    }
  }
  return subPermCount[x]
}

/*
---------------------------------------------------------------------------------
---------------------------------------------------------------------------------
---------------------------------------------------------------------------------
*/
func main() {
  globAdapterList := readAdaptersFromFile("../data/day10_input.txt")
  sort.Ints(globAdapterList)
  deviceJoltage := globAdapterList[len(globAdapterList)-1]+3

  //Our (recursive) algorithm is a perfect example of when a Go Map should be used...
  subPermCount[deviceJoltage] = 1 //Actually this works as a terminator. Which is nice.

  //Iterate over defining key = adapter Joltage, sub-count as zero
  for a := range(globAdapterList) {
    subPermCount[globAdapterList[a]] = 0;
  }
  fmt.Printf("Starting subcount Map: %v\n",subPermCount);
  fmt.Printf("The total number of permutations of solutions is %d\n", calc_subpermutations_from_x(0));/*
  ---------------------------------------------------------------------------------
  */
}
