package main
/*
 PROBLEM: Given an input "map" of trees (#) and space (.), which repeats
          to the right, navigate from top to bottom following a set of
          different defined slopes. Calculate the PRODUCT of the number of
          trees encountered for each different slope.
          slopes:   [dX=1,dY=1],[dX=3,dY=1],[dX=5,dY=1],[dX=7,dY=1],[dX=1,dY=2]

(Because this is a superset of the "part1" problem I'll only implement the total
 thing as a Go solution.)

*/
import(
  "os"
  "bufio"
  "log"
)


// ---------------------------------------------------------------------
func runCourse(dx,dy int, course []string) int {
  //starting position:
  x := 0
  y := 0

  //clock / modulo course width - CAUTION, bytes not chars, convert
  c0 := []rune(course[0])
  modX := len(c0)

  //course length:
  finishY := len(course)

  treesHit := 0
  //Course loop
  treeChar := rune('#')  //AAARRRGHGGHG "" = string, '' = char
  for y < finishY {
      cLine := []rune(course[y])
      if cLine[x] == treeChar {
        treesHit += 1
      }

      //incrememnt position
      y = y + dy
      x = (x + dx) % modX
  }
  return treesHit
}



// ---------------------------------------------------------------------
func main() {
  // Load the course in
  file,err := os.Open("../data/day3_input.txt")
  if err != nil {
    log.Fatal(err)
  }
  defer file.Close()

  var course []string
  s := bufio.NewScanner(file)
  for s.Scan() {
    l := s.Text()
    course = append(course,l)
  }

  //Course loaded. Define the slopes to follow
  slopes := [5][2]int{
      {1,1},
      {3,1},
      {5,1},
      {7,1},
      {1,2},
  }

  //Run the analysis for each slope
  treeProduct := 1
  for run := range slopes {
    slope := slopes[run]
    print("Run ", run, " (dX ", slope[0], ", dY ", slope[1],")")
    treesHit := runCourse(slope[0],slope[1],course)
    print(" hit ", treesHit, " trees\n")
    treeProduct = treeProduct * treesHit
  }

  print("\nTotal TreeProduct: ", treeProduct, "\n")
}
