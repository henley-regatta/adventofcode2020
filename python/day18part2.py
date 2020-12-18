#!/usr/bin/python3
#
# My solution for Day 18 Part 2. V.similar to Part 1 but addition/multiplication
# precedence is inverted from expectations.
#
# PROBLEM
#    Evaluate some mathematical statements with a custom order-of-precedence:
#      * Normal evaluation is left-to-right.
#      * However, addition has precedence over multiplication - a "stack" of
#        equal-precedence operations should see the additions processed before
#        any multiplications.
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

#Control some detailed output logging
debug=False

#Actual data.
inputfile = "../data/day18_input.txt"

#Test data
dummycalc=[]
expectedAnswer=[]
dummycalc.append("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
expectedAnswer.append(23340)
dummycalc.append("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
expectedAnswer.append(669060)
dummycalc.append("5 + (8 * 3 + 9 + 3 * 4 * 3)")
expectedAnswer.append(1445)
dummycalc.append("2 * 3 + (4 *5)")
expectedAnswer.append(46)
dummycalc.append("1 + (2 * 3) + (4 * (5 + 6))")
expectedAnswer.append(51)
dummycalc.append("(1 + 2) * 3 + 4")
expectedAnswer.append(21)
dummycalc.append("1 + (2 * 3) + 4")
expectedAnswer.append(11)
dummycalc.append("1 + 2 * 3 + 4")
expectedAnswer.append(21)
dummycalc.append("1 + 2 + 3 + 4")
expectedAnswer.append(10)


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
# Construct an execution sequence for the calculations using the precedence rules
def psuedo_rpn(exp) :
    acc=0
    op='nul'
    calcStack =[]
    while len(exp) > 0 :
        t = exp.pop(0)
        if debug : print(f"(t:{t})",end="")
        if t == 'openP' :
            vb = psuedo_rpn(exp)
            calcStack.append(vb)
        elif t == 'closeP' :
            acc = evaluate_stack(calcStack)
            return acc
        elif t == 'add' :
            calcStack.append(t)
        elif t == 'multiply' :
            acc = evaluate_stack(calcStack)
            calcStack = [ acc ]
            calcStack.append(t)
        elif isinstance(t,int) :
            calcStack.append(t)
        else :
            print(f"+++ Unrecognised token {t}, remaining: {exp}")
            print(type(t))
            exit(2)

    return evaluate_stack(calcStack)

################################################################################
def evaluate_stack(calcStack) :
    if debug : print(f">evaluate_stack : {calcStack}")
    acc=calcStack.pop()
    if len(calcStack) > 1 :
        while len(calcStack) > 0 :
            op = calcStack.pop()
            vb = calcStack.pop()
            if debug : print(f"(subop: {acc} {op} {vb})",end="=")
            if op == 'multiply' :
                acc *= vb
            else :
                acc += vb
            #print(f"{acc}")
    if debug : print(f"<evaluate_stack: {acc}")
    return acc

################################################################################
################################################################################
################################################################################
if __name__ == '__main__' :

    print("-"*30, " SELF TEST ", "-"*30)

    #No point doing the data unless we can pass the tests...
    passedTests = 0
    failedTests = 0
    takenTests = 0
    while len(dummycalc)>0 and len(expectedAnswer)>0 :
        takenTests +=1
        testSum=dummycalc.pop()
        expect = expectedAnswer.pop()

        expression=tokenise_input(testSum)
        result = psuedo_rpn(expression)
        if result != expect :
            print(f"FAILED TEST: Expression {testSum} expected = {expect}, calculated = {result}")
            failedTests += 1
        else :
            print(f"PASSED TEST: Expression {testSum} expected = {expect}, calculated = {result}")
            passedTests +=1

    print(f"TESTING COMPLETE: {takenTests} tests executed with {passedTests} OK, {failedTests} FAILED")
    if failedTests > 0 :
        print("(Aborting until test suite passed)")
        exit(1)

    print("-"*30, " PART TWO EXECUTION ", "-"*30)
    runningSum = 0
    with open(inputfile,"r") as sums :
        for sum in sums:
            expression = tokenise_input(sum.strip())
            result = psuedo_rpn(expression)
            runningSum += result
    print(f"PART ONE ANSWER: {runningSum}")
