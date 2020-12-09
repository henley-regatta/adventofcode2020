package main
/*
# PROBLEM:
#     Given an "XMAS" Cypher that operates as:
#      - Receive a preamble of "Y" (=25 in this problem) numbers
#      - All numbers after this preamble should be the sum of 2
#        distinct numbers in the preceeding Y numbers
#
#      Report the first number in the input that does NOT conform
#      to this criteria.
#
#      Find a contiguous set of numbers that sum to this non-conforming
#      number.
#
#      Sum the Smallest and the Largest numbers in this contiguous list.
#      Report this number.
*/
import (
  "os"
  "log"
  "bufio"
  "strconv"
  "fmt"
  "sort"
)

//config vars.
const inputfilename string = "../data/day9_input.txt"
const lookback int         = 25

/*
-------------------------------------------------------------------------------
*/
func readNumberListFromFile(filename string) []int {
  var numberlist []int

  fh,err := os.Open(filename)
  if err != nil {
    log.Fatal(err)
  }
  defer fh.Close()

  s := bufio.NewScanner(fh)
  for s.Scan() {
    l := s.Text()
    num, _ := strconv.Atoi(l)
    numberlist = append(numberlist,num)
  }

  return numberlist
}

/*
-------------------------------------------------------------------------------
*/
func num_can_be_summed_from_lookback(target int, lookback []int) bool {
  for i := range lookback {
    for j := range lookback {
      if i == j {
        continue
      }
      if lookback[i]+lookback[j] == target {
        return true
      }
    }
  }
  return false
}

/*
-------------------------------------------------------------------------------
*/
func find_first_unfactored_num(lookback int, numlist []int) int {
  for i,target := range numlist {
    if i<lookback {
      continue
    }
    if ! num_can_be_summed_from_lookback(target,numlist[i-lookback:i]) {
      return target
    }
  }
  return -1
}

/*
-------------------------------------------------------------------------------
This is a less-naieve algorithm to search a list for the match, which should
execute in O(n) instead of O(n^2) of the above approach. It marches a head,tail
of indexes up the list until it finds a range that captures the sum to target
*/
func better_find_range_for_matching_sum(target int, numlist []int) []int {
  i := 0
  j := 1
  runningCount := numlist[i]
  for j<len(numlist) {
    if runningCount == target {
      return numlist[i:j]
    } else if runningCount > target {
      runningCount = runningCount - numlist[i]
      i++
    } else {
      runningCount += numlist[j]
      j++
    }
  }
  fmt.Println("You should not have gotten here. I can't find any subranges that sum to target")
  return []int{-1}
}

/*
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
*/
func main() {
  numberlist := readNumberListFromFile(inputfilename)
  fmt.Printf("Read %d numbers from %s\n",len(numberlist),inputfilename)
  //This gives the answer to Part 1 of the day's challenge (which is input to part 2)
  first_unfactored_num := find_first_unfactored_num(lookback,numberlist)
  fmt.Printf("The first unfactored number from lookback is %d\n",first_unfactored_num)
  sumlist := better_find_range_for_matching_sum(first_unfactored_num,numberlist)
  fmt.Printf("Found sum range: %v\n", sumlist)
  sort.Ints(sumlist)
  fmt.Printf("The smallest number is %d, the largest is %d and the sum of these is %d\n",
      sumlist[0],
      sumlist[len(sumlist)-1],
      sumlist[0] + sumlist[len(sumlist)-1])

}
