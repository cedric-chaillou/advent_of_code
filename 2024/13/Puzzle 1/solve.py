#!/usr/bin/env python3

import time
from collections import namedtuple
import re

def get_test_file_path() :
    return "tests.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( _file_path, _as_lines = True ) :
    with open( _file_path, 'r' ) as f :
        if ( _as_lines ) :
            data = f.readlines()
        else :
            data = f.read()
    return data

button_re = re.compile( r"^Button (?P<name>[AB]): X(?P<x>[-+]\d+), Y(?P<y>[-+]\d+)$" )
prize_re = re.compile( r"^Prize: X=(?P<x>[-+]?\d+), Y=(?P<y>[-+]?\d+)$" )

Button = namedtuple( "Button", [ "name", "x", "y", "cost" ] )
Prize = namedtuple( "Prize", [ "x", "y" ] )
Machine = namedtuple( "Machine", [ "id", "a", "b", "prize" ] )

COST_A = 3
COST_B = 1

def parse_data( str_data, verbose = False ) :
    machines = []
    for i in range( 0, len(str_data), 4 ) :
        if verbose :
            print( f"Lines #{i} => #{i+3}" )
        match = button_re.match( str_data[i].strip() ).groupdict()
        button_a = Button( name = match["name"], x=int(match["x"]), y=int(match["y"]), cost=COST_A )
        if verbose :
            print( f"Button A: {button_a}" )
        match = button_re.match( str_data[i+1].strip() ).groupdict()
        button_b = Button( name = match["name"], x=int(match["x"]), y=int(match["y"]), cost=COST_B )
        if verbose :
            print( f"Button B: {button_b}" )
        match = prize_re.match( str_data[i+2].strip() ).groupdict()
        prize = Prize( x=int(match["x"]), y=int(match["y"]) )
        if verbose :
            print( f"Prize: {prize}" )
        machine = Machine( id=i//4, a=button_a, b=button_b, prize=prize )
        print( f"New machine: {machine}" )
        machines.append( machine )
    print( f"Nb of machines: {len(machines)}" )
    return machines

def vectors_colinear( vector_a, vector_b ) :
    return vector_a.x * vector_b.y == vector_a.y * vector_b.x

def solve_machine( machine, verbose = False ) :
    print( f"Solving for machine #{machine.id}" )
    # system of 2 equations with 2 unknown variables :
    # (1) a.x * press_a + b.x * press_b = prize.x
    # (2) a.y * press_a + b.y * press_b = prize.y
    # solving for press_a, press_b...
    press_a, press_b, solved = 0, 0, 0
    if vectors_colinear( machine.a, machine.b ) :
        if verbose :
            print( f"Buttons A & B vectors are colinear: cannot solve the 'classical' way" )
        if vectors_colinear( machine.a, machine.prize ) :
            # equation (1) <=> equation (2)
            # need to solve equation (1) as a diophantine equation
            if verbose :
                print( f"Prize vector is colinear with buttons A & B" )
                print( f"TODO: Solving a diophantine equation..." )
        else :
            # no possible solution
            if verbose :
                print( f"Prize vector is NOT colinear with buttons A & B: no possible solution" )
    else :
        # only one possible solution:
        # press_a = ( b.x*prize.y - b.y*prize.x ) / ( b.x*a.y - b.y*a.x )
        # press_b = ( a.y*prize.x - a.x*prize.y ) / ( b.x*a.y - b.y*a.x )
        # however, we only accept integers as solutions
        divisor = machine.b.x * machine.a.y - machine.b.y * machine.a.x
        num_press_a = machine.b.x * machine.prize.y - machine.b.y * machine.prize.x
        num_press_b = machine.a.y * machine.prize.x - machine.a.x * machine.prize.y
        if num_press_a % divisor == 0 and num_press_b % divisor == 0 :
            # unique integer solution ( press_a, press_b )
            press_a = num_press_a // divisor
            press_b = num_press_b // divisor
            solved = 1
            if verbose :
                print( f"Solution found: {press_a} presses on button A, {press_b} presses on button B" )
        else :
            # unique real solution ( press_a, press_b )
            # at least one is not an integer !
            if verbose :
                print( f"Unique solution exists but nb of presses found are not integers!" )
    if press_a > 100 or press_b > 100 :
        # no more than 100 presses per button to win...
        if verbose :
            print( f"More than 100 presses for at least one button: cancelling the solution" )
        press_a, press_b, solved = 0, 0, 0
    cost = press_a * machine.a.cost + press_b * machine.b.cost
    print( f"Cost: {cost}, solved: {solved}" )
    return cost, solved

def do_problem( str_data, verbose = False ) :
    machines = parse_data( str_data, verbose )
    total_cost = 0
    nb_solved = 0
    for machine in machines :
        cost, solved = solve_machine( machine, verbose )
        total_cost += cost
        nb_solved += solved
    print( f"Need {total_cost} tokens for {nb_solved} machines solved out of {len(machines)}" )

def do_tests() :
    str_data = get_file_content( get_test_file_path(), True )
    do_problem( str_data, True )

def do_input() :
    str_data = get_file_content( get_input_file_path(), True )
    do_problem( str_data, False )

def main() :
    start = time.time()
    #do_check(  )
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
