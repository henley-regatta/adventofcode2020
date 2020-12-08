package main

/*
 problem spec:
     given a file containing a list of numbers, find the TWO numbers in that
     list that sum to 2020.
     Return the product of those two numbers.
*/

import(
  "fmt"
  "os"
  "log"
  "bufio"
  "strconv"
)

func main() {
  file,err := os.Open("../data/day1_input.txt")
  if err != nil {
    log.Fatal(err)
  }
  defer file.Close()

  numlist := []int{}
  scanner := bufio.NewScanner(file)
  for scanner.Scan() {
    numStr := scanner.Text()
    num, _ := strconv.Atoi(numStr)
    numlist = append(numlist,num)
  }

  if err := scanner.Err(); err != nil {
    log.Fatal(err)
  }

  /* My whole python solution to this problem was 22 lines. Here we are at
     line 37 having just read the file in.... */
  for i := 0; i < len(numlist); i++ {
    x := numlist[i]
    for j := 0; j < len(numlist); j++ {
      if i == j {
        continue /*don't self-evaluate*/
      }
      if x + numlist[j] == 2020 {
        fmt.Print(x , " + ", numlist[j], " = 2020 with product ", x*numlist[j], "\n")
      }
    }
  }

}
