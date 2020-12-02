package main

import "testing"


func TestDay1Part2(t *testing.T) {
    for i := 0; i< 10000; i++ {
        comp := day2part1()
        expected := int(607)
        if(comp != expected) {
            t.Errorf("WRONG ANSWER!")
        }
    }
}

