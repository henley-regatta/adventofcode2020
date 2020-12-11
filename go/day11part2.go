package main
/*
# PROBLEM:
#     You are given an input "Seat Map for a ferry"
#     (.=floor, L=seat, #=occupied seat). New arrivals will change seat state
#     according to rules similar to (BUT DIFFERENT FROM) Conway's Life
#       * Seat will be OCCUPIED (L->#) IF no "visible" seats are occupied.
#         (up,down,left,right and diagonals - 8 places)
#       * Seat will be VACATED (#->L) IF 5 or more "visible" seats are OCCUPIED
#       * No other seat will be modified.
#
# The "Visibility" rule applies thus:
#   From your position, iterate away in the given direction ignoring floor.
#   The state of the first seat encountered - not floor - determines the occupancy.
#
#  Iterate over a given input seat map applying the rules above until a steady-state
#  is arrived at. How many seats are occupied?

This Go version implements Day 11 part 2 because it's got the "harder" Visibility
rules. After my experience with the Python version, this is an exercise in trying
to manage the data in a more readable way.

NOTE: I know passing my "big" structure around as parameters everywhere isn't brilliant,
     but I've done my looking and I see "don't pass slices by reference" so I'm
     relying on the compiler's copy-on-write optimisations to save my skin here.
*/
import (
  "os"
  "log"
  "bufio"
  "fmt"
  "strings"
)

//The Seatmap is where we hold the (iterable) state of the seating.
//Given the analysis we do, there's not much point changing it's format from
//the read in value. . But we do need globals for the max X,Y values
var maxXY = map[rune]int{ 'x' : 0, 'y' : 0}

//A static to define which directions we'll look in:
var lookDirections = [8][2]int{
  {-1,-1},
  {-1,0},
  {-1,+1},
  {0,-1},
  {0,+1},
  {+1,-1},
  {+1,0},
  {+1,+1},
}

/*
---------------------------------------------------------------------------------
*/
func readSeatmapFromFile(filename string) []string {
  var seatmap  []string
  fh,err := os.Open(filename)
  if err != nil {
    log.Fatal(err)
  }
  defer fh.Close()
  s := bufio.NewScanner(fh)
  for s.Scan() {
    row := strings.TrimSuffix(s.Text(),"\n")
    if len(row)>0 {
      seatmap = append(seatmap,row)
    }
  }
  //Update the maxXY for later references
  maxXY['y'] = len(seatmap)-1
  maxXY['x'] = len(seatmap[0])-1
  return seatmap
}

/*
---------------------------------------------------------------------------------
Little vanity function for output of seatmap state.
*/
func pprintSeatmap(seatmap []string) {
  for l := range seatmap {
    fmt.Println(seatmap[l])
  }
}

/*
---------------------------------------------------------------------------------
Helper function to count the occupied seats on the map. Acts as proxy for
detecting stasis
*/
func countOccupiedSeats(seatmap []string) int {
  occupiedSeats:=0
  for y := range seatmap {
    for x := range seatmap[y] {
      if seatmap[y][x] == '#' {
        occupiedSeats++
      }
    }
  }
  return occupiedSeats
}

/*
---------------------------------------------------------------------------------
Look-around function. Look progressively far away (over floor) for first chair
and return it's state
*/
func lookdirection(x,y,dx,dy int, seatmap []string) int {
  rv := 0 //default case
    if !(dx==0 && dy==0) {  //Skip special case of "look at ourself"
      foundChair := false
      //iterators
      cx := x
      cy := y
      for !foundChair {
        cx += dx
        cy += dy
        //At this position, what do?
        if cx<0 || cx>maxXY['x'] || cy<0 || cy>maxXY['y'] {
          foundChair = true //strictly we haven't, but we run off the end here anyway
        } else {
          if seatmap[cy][cx] != '.' {
            foundChair = true
            if seatmap[cy][cx] == '#' {  rv = 1  }
          }
        }
      }
    }
  return rv
}

/*
---------------------------------------------------------------------------------
Calculation function. Workout the state at n+1 for position (x,y) given input seatmap
*/
func calculateNewState(x,y int, seatmap []string) byte {
  //By default we return the input value
  retval := seatmap[y][x]
  //The rules of tge game are that we need to calculate the adjacent
  //occupancy from the starting position and mutate the value based on that.
  //First clear out the special case:
  if retval != '.' {
    adjacency := 0
    //In each 8 direction from our position, ignoring floor, find the first
    //seat in that direction and adjacency is that seat's occupied value
    for i := range lookDirections {
        adjacency += lookdirection(x,y,lookDirections[i][0],lookDirections[i][1],seatmap)
    }
    //Decision time. Our rules are thus:
    if adjacency > 4 {
      retval = 'L' //Too busy -> Seat becomes unoccupied
    } else if adjacency == 0 {
      retval = '#' //A nice empty space -> Occupy seat
    }
  }
  //And the default is "stay the same" which we've already captured.
  return retval
}


/*
---------------------------------------------------------------------------------
DRIVER WRAPPER: Given input state (seatmap) calculate output state
nb: slices. Must be passed by value, not reference. Annoyingly.
*/
func iterateSeatmap(inseatmap []string) []string {
  var outseatmap []string
  for y := range inseatmap {
    var newRow []byte
    for x := range inseatmap[y] {
      newRow = append(newRow,calculateNewState(x,y,inseatmap))
    }
    outseatmap = append(outseatmap, string(newRow))
  }
  return outseatmap
}


/*
---------------------------------------------------------------------------------
---------------------------------------------------------------------------------
---------------------------------------------------------------------------------
*/
func main() {
  //seatmap := readSeatmapFromFile("../data/day11_test1.txt")
  seatmap := readSeatmapFromFile("../data/day11_input.txt")
  oldSeatsOccupied := countOccupiedSeats(seatmap)
  iterCount := 0
  fmt.Printf("Ship has %d rows of %d seats each\n",maxXY['y']+1,maxXY['x']+1)
  fmt.Printf("(%03d):[%05d] -----------------------------------------------\n",iterCount,oldSeatsOccupied)
  pprintSeatmap(seatmap)
  reachedStasis := false
  for !reachedStasis {
      iterCount++
      newSeatmap := iterateSeatmap(seatmap)
      newSeatsOccupied := countOccupiedSeats(newSeatmap)
      fmt.Print("\033[H\033[2J]") //ANSI Escape for "clear screen"
      fmt.Printf("(%03d):[%05d] -----------------------------------------------\n",iterCount,newSeatsOccupied)
      pprintSeatmap(newSeatmap)
      if newSeatsOccupied == oldSeatsOccupied {
        reachedStasis = true
      } else {
        oldSeatsOccupied = newSeatsOccupied
        seatmap = newSeatmap
      }
  }
  fmt.Printf("\nReached Stasis after %d iterations. Last Passenger Count was %d\n",iterCount,oldSeatsOccupied)

}
