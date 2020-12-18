#!/usr/bin/python3
#
# My solution for Day 18 Part 1.
#
# PROBLEM
#    Evaluate some mathematical statements with a custom order-of-precedence:
#      * In the absence of parentheses, all operations are evaluted left-to-right.
#      * The normal rules of precedence do not apply ( / an * before + and -)
#      * However, parethenses still exist and work as expected: expressions within
#        a set of () are evaluated first, and the result is applied to the remaining
#        calculation
#
#   Shortcut: The input contains no division, or subtraction. it's + and * only.
#   Shortcut: The data has only single-digit numbers, and 0 does not appear.
#
#   REQUIREMENT: Given an input of calculations, one per line, calculate the SUM
#                of the results of these calculations.
#
import sys

#Actual data.
inputfile = "../data/day18_input.txt"

#Test data. Expected answer is 26
dummycalc = "2 * 3 + (4 *5)"
#Test data. Expected answer is 13632
dummycalc = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
#Test data. Expected answer 12240
dummycalc = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
#Test data. Expected answer 437
dummycalc = "5 + (8 * 3 + 9 + 3 * 4 * 3)"

################################################################################
# We needs a little helper function....
def tokenise_input(inString) :
    expression = []
    #The data is exceptionally well-formed. If a token has length>1, it's because
    #it's a number that starts or finishes with a parenthesis.
    for t in inString :
        if t == ' ' :
            continue
        elif t == '+' :
            expression.append('add')
        elif t == '*' :
            expression.append('multiply')
        elif t == '(' :
            expression.append('openP')
        elif t == ')' :
            expression.append('closeP')
        else :
            #WE CAN ONLY GET AWAY WITH THIS BECAUSE WE'VE SPOTTED THE INPUT
            #CONSISTS OF SINGLE-DIGIT NUMBERS ONLY
            try:
                expression.append(int(t))
            except ValueError :
                print(f"+++ ERROR PARSING {t} - SHOULD BE A DIGIT")
                exit(1)

    return expression

################################################################################
#There is no solution more satisfying than one that works using recursion.
def evaluate_expression(exp) :
    acc = 0
    v = 0
    op = 'nul'
    while len(exp) > 0 :
        t = exp.pop(0)
        print(t,end=',')
        if t == 'openP' :
            v = evaluate_expression(exp)
        elif t == 'closeP' :
            return acc
        elif t == 'multiply' or t == 'add' :
            op = t
        elif isinstance(t, int) :
            if acc==0 :
                acc=t
            else :
                v = t
        else :
            print(f"+++ Unrecognised token {t}")
            print(type(t))
            exit(2)

        #Have we gathered enough tokens to perform an operation yet?
        if v>0 and op != 'nul' :
            if op == 'add' :
                acc = acc + v
            elif op == 'multiply' :
                acc = acc * v
            v=0
            print(f"[acc = {acc}]",end=",")
        #Possibly not but we might have a special-case of front-recursion to handle:
        elif v>0 and acc==0 :
            acc = v
            v = 0

    return acc

################################################################################
################################################################################
################################################################################
if __name__ == '__main__' :
    runningSum = 0
    with open(inputfile,"r") as sums :
        for sum in sums:
            expression = tokenise_input(sum.strip())
            result = evaluate_expression(expression)
            runningSum += result
    print("\n","-"*80)
    print(f"PART ONE ANSWER: {runningSum}")
