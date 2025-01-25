#!/usr/bin/env python3

import time
from collections import namedtuple
import re

def get_test_file_path( i: int = None ) -> str :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() -> str :
    return "input.txt"

def get_file_content( file_path ) -> str :
    print( f"Reading: {file_path}" )
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

# y02: 0
INPUT_RE = re.compile( r"^(?P<name>[\w\d]{3}): (?P<value>[01])$" )
# x00 AND y00 -> z00
GATE_RE = re.compile( r"^(?P<a>[\w\d]{3}) (?P<op>AND|OR|XOR) (?P<b>[\w\d]{3}) -> (?P<name>[\w\d]{3})$" )

Input = namedtuple( "Input", [ "name", "value" ] )
Gate = namedtuple( "Gate", [ "a", "op", "b" ] )

def parse_data( str_data: str, verbose: bool = False ) :
    x: list[str] = []
    y: list[str] = []
    z: list[str] = []
    solved: dict[ str, int ] = dict()
    gates: dict[ str, Gate ] = dict()
    input_mode = True
    for line in str_data.strip().split( "\n" ) :
        if line == "" :
            print( "Empty line" ) if verbose else None
            input_mode = False
        elif input_mode :
            print( f"Input line: {line}" ) if verbose else None
            match = INPUT_RE.match( line ).groupdict()
            name = match[ "name" ]
            value = int( match[ "value" ] )
            solved[ name ] = value
            if name[0] == "x" :
                x.append( name )
            elif name[0] == "y" :
                y.append( name )
        else :
            print( f"Gate line: {line}" ) if verbose else None
            match = GATE_RE.match( line ).groupdict()
            name = match[ "name" ]
            gate = Gate( match[ "a" ], match[ "op" ], match[ "b" ] )
            gates[ name ] = gate
            solved[ name ] = None
            if name[0] == "z" :
                z.append( name )
    x = tuple( sorted( x, reverse=True ) )
    y = tuple( sorted( y, reverse=True ) )
    z = tuple( sorted( z, reverse=True ) )
    x_value = "".join( str( solved[i] ) for i in x )
    y_value = "".join( str( solved[i] ) for i in y )
    print( f"x input: 0b{x_value} = {int( x_value, base=2 )}" )
    print( f"y input: 0b{y_value} = {int( y_value, base=2 )}" )
    if verbose :
        print( f"z output gates: {z}" )
    return x, y, z, gates, solved

def solve( name: str, gates: dict[ str, Gate ], solved: dict[ str, int ], verbose: bool ) -> int :
    if solved[ name ] is None :
        gate = gates[ name ]
        a_value = solve( gate.a, gates, solved, verbose )
        b_value = solve( gate.b, gates, solved, verbose )
        if gate.op == "AND" :
            solved[ name ] = a_value & b_value
        elif gate.op == "OR" :
            solved[ name ] = a_value | b_value
        elif gate.op == "XOR" :
            solved[ name ] = a_value ^ b_value
        if verbose:
            print( f"Computed value for gate {name}: {gate.a} {gate.op} {gate.b} = {solved[ name ]}" )
    return solved[ name ]

def do_problem( str_data: str, verbose: bool = False ) :
    x, y, z, gates, solved = parse_data( str_data, verbose )
    output = ""
    for name in z :
        output += str( solve( name, gates, solved, verbose ) )
    print( f"z output: 0b{output} = {int( output, base=2 )}" )
    print( f"END" )

def do_tests( i: int = None ) :
    str_data = get_file_content( get_test_file_path( i ) )
    do_problem( str_data, True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, False )

def main() :
    start = time.time()
    #do_tests(1)
    #do_tests(2)
    #do_tests(3)
    #do_tests(4)
    #do_tests(5)
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
