//Since we're being silly, attempt the solution in Rust too.

/*
 problem spec:
     given a file containing a list of numbers, find the TWO numbers in that
     list that sum to 2020.
     Return the product of those two numbers.

     Data is in file "day1_input.txt"
*/

use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let f = File::open("day1_input.txt").expect("Unable to open file");
    let f = BufReader::new(f);

    let mut elem: Vec<i32> = Vec::new();
    for line in f.lines() {
        let line = line.expect("Unable to read line");
        let num: i32 = line.parse().unwrap();
        elem.push(num)
    }

    print!("File contained {} lines\n", elem.len());

    for i in 0..elem.len() {
        let x = elem[i];
        for j in 0..elem.len() {
            if i != j {
                if x + elem[j] == 2020 {
                    print!("{} + {} = 2020 with product {}\n", x, elem[j], x*elem[j]);
                }
            }
        }
    }
}
