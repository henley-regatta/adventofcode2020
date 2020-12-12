package main
/*
# PROBLEM:
#     Given a list of input instructions of form <I><Distance/Degrees>, where
#        I = N (North)| S (South) | E (East) | W (West)
#        I = L (Left) | R (Right) | F (Forward)
#
#     WHERE ALL INSTRUCTIONS REFER TO THE RELATIVE POSITION OF A WAYPOINT,
#     (N/E/S/W move the waypoint those positions, L/R rotate the waypoint about
#     the ship position)
#     with the exception of F which moves the ship to the waypoint <n> times
#    (the waypoint maintains it's relative position to the ship at all times)
#     And a starting position of (0,0), facing East, waypoint at (10 east, 1 north):
#        a) Calculate the final position by following the instructions
#        b) Compute the "Manhattan Distance" (sum of absolute east/west + north/south positions)
#
#   NOTE: Rotating a vector needs Maths. If you're doing it properly. But we can
#         cheat because all the angles given are multiples of 90 degrees. Fortunately.

This is going to be a reasonably straight translation from the Python version
of my answer too.
*/
import(
  "os"
  "log"
  "bufio"
  "fmt"
  "strings"
  "strconv"
)

//There's a limited set of instructions we support so enumerate them:
type Instruction int
const (
  North Instruction = iota
  East
  South
  West
  Left
  Right
  Forward
)

//We have 2 types of data, arguably both are just simple Maps but...
type ACommand struct {
  ins Instruction
  parm int
  valid bool
}
type StateVector struct {
  shipNorth int
  shipEast  int
  wpNorth   int
  wpEast    int
}

//-----------------------------------------------------------------------------
//Helper function for showing the Instructions:
func (i Instruction) String() string {
  return [...]string{"North","East","South","West","Left","Right","Forward"}[i]
}

// Oh wow, there's no built-in Abs function for ints...
func intAbs(x int) int {
  if x<0 {
    return -1 * x
  }
  return x
}


/*
-------------------------------------------------------------------------------
*/
func parseInstruction(insTxt string) ACommand {
  p,_ := strconv.Atoi(insTxt[1:])  //Extract the number parameter
  outCommand := ACommand{
    ins   : Forward,
    parm  : p,
    valid : true,
  }
  i := insTxt[0]
  switch i {
    case 'N' : { outCommand.ins = North }
    case 'E' : { outCommand.ins = East }
    case 'S' : { outCommand.ins = South }
    case 'W' : { outCommand.ins = West }
    case 'L' : { outCommand.ins = Left}
    case 'R' : { outCommand.ins = Right}
    case 'F' : { outCommand.ins = Forward}
    default  : {
      outCommand.valid = false;
      log.Fatal("Unrecognised Command: " + string(i))
    }
  }
  return outCommand
}


/*
-------------------------------------------------------------------------------
*/
func rotateWP(inState StateVector,dir Instruction,degrees int) StateVector {
  outState := inState
  //Some simplification:
  if degrees==270 {
    degrees=90
    if dir==Left {
      dir=Right
    } else {
      dir=Left
    }
  }
  //Now process the state vector update:
  if degrees==180 {
    outState.wpNorth = -1 * inState.wpNorth
    outState.wpEast  = -1 * inState.wpEast
  } else if degrees==90 {
    if dir==Left {
      outState.wpNorth = inState.wpEast
      outState.wpEast  = -1 * inState.wpNorth
    } else {
      outState.wpNorth = -1 * inState.wpEast
      outState.wpEast  = inState.wpNorth
    }
  } else {
    log.Fatal("Unrecognised Rotation Command")
  }

  return outState
}



/*
-------------------------------------------------------------------------------
*/
func updateStateVector(inState StateVector, cmd ACommand) StateVector {
  outState := inState
  switch cmd.ins {
    //These commands are "easy" and just move the waypoint:
    case North : { outState.wpNorth = inState.wpNorth + cmd.parm}
    case East  : { outState.wpEast  = inState.wpEast  + cmd.parm}
    case South : { outState.wpNorth = inState.wpNorth - cmd.parm}
    case West  : { outState.wpEast  = inState.wpEast  - cmd.parm}
    //Left and Right require transformation of the Waypoint vector
    case Left  : { outState = rotateWP(inState,cmd.ins,cmd.parm)}
    case Right  : { outState = rotateWP(inState,cmd.ins,cmd.parm)}
    //Forward is the only command that moves the ship, to the Waypoint <parm>
    //times:
    case Forward : {
      outState.shipNorth = inState.shipNorth + (cmd.parm * inState.wpNorth)
      outState.shipEast  = inState.shipEast  + (cmd.parm * inState.wpEast)

    }
    default : { log.Fatal("Cannot execute unsupported command")}
  }


  return outState
}


/*
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
The instructions here are simple enough to not really justify separating
out the load-process-output phases, so main() carries more weight than normal.
*/
func main() {
  infile := "../data/day12_input.txt"
  //infile := "../data/day12_test.txt"

  //Here's the master state vector we'll update throughout.
  stateVector := StateVector {
    shipNorth : 0,
    shipEast  : 0,
    wpNorth   : 1,
    wpEast    : 10,
  }

  //boilerplate file handling:
  fh,err := os.Open(infile)
  if err != nil {
    log.Fatal(err)
  }
  defer fh.Close()
  s := bufio.NewScanner(fh)

  //Here's the main loop. Each input line is an instruction to follow so
  //we update the stateVector as we go

  validInstructions := 0

  for s.Scan() {
    insText := strings.TrimSuffix(s.Text(),"\n")
    if len(insText)>0 {
      command := parseInstruction(insText)
      fmt.Printf("(%5s):",insText)
      if command.valid {
        stateVector = updateStateVector(stateVector,command)
        fmt.Printf("%v\n", stateVector)
        validInstructions++
      }
    }
  }
  manhattanDistance := intAbs(stateVector.shipNorth) + intAbs(stateVector.shipEast)
  fmt.Printf("Final Ship Position after %d instructions (%04d,%04d) has Manhattan Distance = %d\n",
      validInstructions,
      stateVector.shipNorth,
      stateVector.shipEast,
      manhattanDistance,
  )
}
