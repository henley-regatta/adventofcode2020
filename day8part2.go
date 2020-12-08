package main
/*
# PROBLEM:
#     Given a simple machine code system with 3 instructions:
#       acc <signedInt>   - Add the parameter to the single register, ACC
#       jmp <signedInt>   - Move execution <signedInt> steps forward/backward
#       nop <signedInt>   - Do nothing, step to next instruction.
#
#    ... Change the value of just one "jmp" or "nop" instruction (by inverting
#        "jmp" to "nop" or vica-versa with the same parameters) such that the
#        program terminates (jumps/advances beyond the instruction set). Report
#        the value of ACC immediately prior to termination.
# DISCUSSION:
#      * There is no point changing "jmp" or "nop" instructions that were never
#      visited by the original looping code (as they cannot affect the outcome)
*/
import(
  "os"
  "log"
  "bufio"
  "strconv"
  "strings"
  "fmt"
)

//The actual instructions are an enum:
type Mnemonic int
const (
  acc Mnemonic = iota
  jmp
  nop
)

//The instruction construct we need is a struct using this:
//(and as we go we'll build slices of this up as our list of instructions)
type Instruction struct {
  ins Mnemonic
  parm int
  visited bool
}

//This is sort of a hack but it's a good way of encapsulating the results of a
//execution run of a given instruction set:
type ExecutionResults struct {
  looped bool
  pcr    int
  acc    int
  executedInstructions []int
}

// --------------------------------------------------------------------------------
func executeInstructionSet(instructions []Instruction) ExecutionResults {
  res := ExecutionResults{looped : false, pcr : 0, acc : 0}
  maxPcr := len(instructions)
  //reset visited count for all instructions
  for i := range instructions {
    instructions[i].visited = false
  }
  //EXECUTE THE CODE:
  for !res.looped {
    if res.pcr >= maxPcr {
       break //Normal program exit point
    } else if instructions[res.pcr].visited == true  {
       res.looped = true
       break // Program has looped, mark as such and quit
    }
    //Mark this instruction as visited
    instructions[res.pcr].visited = true
    res.executedInstructions = append(res.executedInstructions,res.pcr)
    //Execute the instruction:
    switch instructions[res.pcr].ins {
      case acc : {
        res.acc += instructions[res.pcr].parm
        res.pcr +=1
      }
      case jmp : {
        res.pcr += instructions[res.pcr].parm
      }
      case nop : {
        res.pcr+=1
      }
      default : {
        fmt.Printf("Invalid instruction at pcr=%d : %#v\n",res.pcr,instructions[res.pcr])
        log.Fatal(res.pcr)
      }
    }
  }
  return res
}

// --------------------------------------------------------------------------------
// helper function for mnemonic type
func (m Mnemonic) String() string {
  return [...]string{"acc","jmp","nop"}[m]
}

// --------------------------------------------------------------------------------
func parseFileIntoInstructionSet(filename string) []Instruction {
  var instructions []Instruction

  fh,err := os.Open(filename)
  if err != nil {
    log.Fatal(err)
  }
  defer fh.Close()

  s := bufio.NewScanner(fh)
  for s.Scan() {
    l := s.Text()
    //Split on space
    elem := strings.Split(l," ")
    //first part is an instruction
    ins := Instruction{visited : false}
    switch elem[0] {
      case "acc" : { ins.ins = acc }
      case "jmp" : { ins.ins = jmp }
      case "nop" : { ins.ins = nop }
      default :{
        log.Fatal("Invalid instruction in src file: " + l)
      }
    }
    //second part is a numeric parameter. Always.
    ins.parm,_ = strconv.Atoi(elem[1])
    instructions = append(instructions,ins)
  }

  return instructions
}

// --------------------------------------------------------------------------------
// --------------------------------------------------------------------------------
// --------------------------------------------------------------------------------
func main() {
  instructionSet := parseFileIntoInstructionSet("day8_input.txt");
  fmt.Printf("Instruction set has %d instructions\n",len(instructionSet))

  //Run the code once to gather the set of executed instructions
  firstRunRes := executeInstructionSet(instructionSet)
  fmt.Printf("First run looped at PCR = %d after %d instructions. ACC = %d\n",
           firstRunRes.pcr,
           len(firstRunRes.executedInstructions),
           firstRunRes.acc)

  //The values in firstRunRes.executedInstructions now form the input for
  //values to swap jmp/nop from and retry:
  for i := range firstRunRes.executedInstructions {
    ti := firstRunRes.executedInstructions[i]
    orgIns := instructionSet[ti].ins
    tryChange := false
    switch orgIns {
      case jmp : {
        instructionSet[ti].ins = nop;
        tryChange = true
      }
      case nop : {
        instructionSet[ti].ins = jmp;
        tryChange = true
      }
    }
    if tryChange {
      newRunRes := executeInstructionSet(instructionSet)
      if newRunRes.looped {
        /*
        fmt.Printf("Changing instruction %d to %s didn't help; looped after %d instructions at %d\n",
          ti,
          instructionSet[ti].ins,
          len(newRunRes.executedInstructions),
          newRunRes.pcr)
        */
        instructionSet[ti].ins = orgIns
      } else {
        fmt.Printf("SUCCESS! Changing instruction %d to %s caused termination with ACC = %d\n",
          ti,
          instructionSet[ti].ins,
          newRunRes.acc)
        break;
      }
    }
  }
}
