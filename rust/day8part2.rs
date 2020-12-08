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
use std::{
    fs::File,
    io::{prelude::*, BufReader},
    path::Path,
};

//Fortunately, the instruction set required is quite small:
//nb: this makes output easier:
#[derive(Copy, Clone, Debug)]
enum Mnemonic {
    Acc,
    Jmp,
    Nop
}

/*
--------------------------------------------------------------------------------------------------
*/
//Meaning the values required to be stored as similarly small:
#[derive(Copy, Clone, Debug)]
struct Instruction {
    ins: Mnemonic,
    parm: isize,    //Unlike much of our working, this has to be signed....
    visited: bool
}

impl Instruction {
    fn new(ins_text: &str, parm_text: &str) -> Self {
        //TODO : There *has* to be a better way to instantiate than this, surely?
        let mut ins: Instruction = Instruction{ins: Mnemonic::Acc, parm: 0, visited: false};
        ins.add_ins(ins_text);
        ins.add_parm(parm_text);
        return ins;
    }
    fn mark_visited(&mut self) {
        self.visited = true;
    }
    fn is_visited(&self) -> bool {
        return self.visited;
    }
    fn add_ins(&mut self, opc_text: &str) {
        match opc_text {
            "acc" => self.ins = Mnemonic::Acc,
            "jmp" => self.ins = Mnemonic::Jmp,
            "nop" => self.ins = Mnemonic::Nop,
            _ => println!("OPCode {} does not match recognised opcodes", opc_text)
        }
    }
    fn add_parm(&mut self, parm_text: &str) {
       let p_val : isize = parm_text.parse().unwrap();
       self.parm = p_val;
    }
    fn copy_ins(&self) -> Instruction {
        return Instruction {
            ins : self.ins,
            parm : self.parm,
            visited: self.visited
        }
    }
}
/*
--------------------------------------------------------------------------------------------------
*/
//As for the Go version, executing a program is easier if we can return a
//results structure
#[derive(Clone, Debug)]
struct ExecutionResult {
    pcr: isize,
    acc: isize,
    looped: bool,
    visited_instructions: Vec<usize>
}
/*
--------------------------------------------------------------------------------------------------
*/
fn execute_instruction_list(instructions: &Vec<Instruction>) -> ExecutionResult {
    let mut r : ExecutionResult = ExecutionResult{
        pcr : 0,
        acc: 0,
        looped: false,
        visited_instructions: vec![]
    };
    //We need to work off a copy of the instruction list, sadly, because we need to
    //reset the visited state on change.
    let mut execute_list : Vec<Instruction> = Vec::new();
    for i in instructions {
        execute_list.push(i.copy_ins());
    }

    //OK HERE WE GO....
    let max_pcr = execute_list.len();
    while !r.looped {
        //we need pcr to be an isize for arithmatic but usize reference.
        let pcr_as_u : usize = r.pcr as usize;
        //Check for program termination conditions
        if pcr_as_u >= max_pcr {
            break //Normal - good - program exit point
        } else if execute_list[pcr_as_u].is_visited() {
            r.looped = true; //We've been here before -> quit.
            break;
        }
        //OK, execute the instruction at hand
        execute_list[pcr_as_u].mark_visited();
        r.visited_instructions.push(pcr_as_u);
        match execute_list[pcr_as_u].ins {
            Mnemonic::Acc => {
                r.acc += execute_list[pcr_as_u].parm;
                r.pcr += 1;
            }
            Mnemonic::Jmp => {
                r.pcr += execute_list[pcr_as_u].parm;
            }
            Mnemonic::Nop => {
                r.pcr += 1;
            }
        }
    }
    return r;
}

/*
--------------------------------------------------------------------------------------------------
*/
fn read_instructions_from_file(f_name: impl AsRef<Path>) -> Vec<Instruction> {
    let file = File::open(f_name).expect("Unable to open file");
    let b = BufReader::new(file);

    let mut instructions : Vec<Instruction> = Vec::new();
    for l in b.lines() {
        let l = l.expect("Unable to read line from file");
        //split line by space
        let part : Vec<&str> =  l.split(" ").collect();
        let instr : Instruction = Instruction::new(part[0],part[1]);
        instructions.push(instr)
    }
    return instructions
}

/*
--------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------
*/

fn main() {
    let mut instructions = read_instructions_from_file("../data/day8_input.txt");
    println!("Read {} instructions from file", instructions.len());

    //First run is a bit different. Do it and see what we get
    let first_run_res = execute_instruction_list(&instructions);
    println!("First run quit at pcr = {} with acc = {} after {} instructions",
        first_run_res.pcr,
        first_run_res.acc,
        first_run_res.visited_instructions.len());

    //OK so now we need to loop over the visited instructions mutating jmp to nop and vica-versa
    //until we get a good completion.
    for m in first_run_res.visited_instructions {
        let should_test : bool;
        let org_ins : Mnemonic = instructions[m].ins;
        match org_ins {
            Mnemonic::Jmp => {
                should_test = true;
                instructions[m].ins = Mnemonic::Nop;
            }
            Mnemonic::Nop => {
                should_test = true;
                instructions[m].ins = Mnemonic::Jmp;
            }
            _ => {
                should_test = false;
            }
        }
        if should_test {
            let test_run = execute_instruction_list(&instructions);
            if test_run.looped {
                /*
                println!("Test run mutating instruction {} to {:?} failed; looped after {} instructions",
                    m,
                    instructions[m].ins,
                    test_run.visited_instructions.len());
                */
                instructions[m].ins = org_ins;
            } else {
                println!("SUCCESS! Mutated instruction {} to {:?} with normal program termination. Final acc = {}",
                    m,
                    instructions[m].ins,
                    test_run.acc);
                break;
            }
        }
    }
}
