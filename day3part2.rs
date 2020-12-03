/*
 PROBLEM: Given an input "map" of trees (#) and space (.), which repeats
          to the right, navigate from top to bottom following a set of
          different defined slopes. Calculate the PRODUCT of the number of
          trees encountered for each different slope.
          slopes:   [dX=1,dY=1],[dX=3,dY=1],[dX=5,dY=1],[dX=7,dY=1],[dX=1,dY=2]

(Because this is a superset of the "part1" problem I'll only implement the total
 thing as a Go solution.)

*/
use std::{
    fs::File,
    io::{prelude::*, BufReader},
    path::Path,
};

// -------------------------------------------------------------------------------------------
fn read_course_to_string_array(f_name: impl AsRef<Path>) -> Vec<String> {
    let file = File::open(f_name).expect("Unable to open file");
    let b = BufReader::new(file);

    b.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect()
}

// -------------------------------------------------------------------------------------------
fn run_slope_on_course(dx: usize, dy: usize, course: &Vec<String>) -> usize {
    //initial position
    let mut x = 0;
    let mut y = 0;

    //iterate width as function of string length modulus, length of the course
    let mod_x = course[0].len();
    let lim_y = course.len();

    let mut trees_hit = 0;
    while y < lim_y {
        //Did we hit a tree?
        if course[y].chars().nth(x).unwrap() == '#' {
            trees_hit += 1;
        }
        //update position
        x = (x + dx) % mod_x;
        y = y + dy;
    }
    return trees_hit;
}

// -------------------------------------------------------------------------------------------
fn main() {
    let course = read_course_to_string_array("day3_input.txt");
    //define the slopes to investigate
    let slopes = [[1,1],[3,1],[5,1],[7,1],[1,2]];
    let mut product_trees_hit = 1;
    for i in 0..slopes.len() {
        let t_hit = run_slope_on_course(slopes[i][0],slopes[i][1],&course);
        println!("Slope {} ({},{}) hit {} trees", i,slopes[i][0],slopes[i][1],t_hit);
        product_trees_hit = product_trees_hit * t_hit;
    }

    println!("Product of trees hit is {}", product_trees_hit)
}
