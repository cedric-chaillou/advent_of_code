#!/usr/bin/env python3

import time
from collections import namedtuple
from itertools import permutations
from functools import cache

def get_test_file_path( i: int = None ) -> str :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() -> str :
    return "input.txt"

def get_file_content( file_path: str ) -> str :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

Coordinate = namedtuple( "Coordinate", [ "x", "y" ] )
Vector = namedtuple( "Vector", [ "dx", "dy" ] )

def get_numeric_pad() -> tuple[ dict[ str, Coordinate ], dict[ Coordinate, str ] ] :
    #   7 8 9
    #   4 5 6
    #   1 2 3
    #     0 A
    pad = {
        "7" : Coordinate( 0, 0 ),
        "8" : Coordinate( 1, 0 ),
        "9" : Coordinate( 2, 0 ),
        "4" : Coordinate( 0, 1 ),
        "5" : Coordinate( 1, 1 ),
        "6" : Coordinate( 2, 1 ),
        "1" : Coordinate( 0, 2 ),
        "2" : Coordinate( 1, 2 ),
        "3" : Coordinate( 2, 2 ),
        "0" : Coordinate( 1, 3 ),
        "A" : Coordinate( 2, 3 ),
    }
    pad_map = dict()
    for char, coord in pad.items() :
        pad_map[ coord ] = char
    return pad, pad_map

def get_directional_pad() -> tuple[ dict[ str, Coordinate ], dict[ Coordinate, str ] ] :
    #     ^ A
    #   < v >
    pad = {
        "^" : Coordinate( 1, 0 ),
        "A" : Coordinate( 2, 0 ),
        "<" : Coordinate( 0, 1 ),
        "v" : Coordinate( 1, 1 ),
        ">" : Coordinate( 2, 1 ),
    }
    pad_map = dict()
    for char, coord in pad.items() :
        pad_map[ coord ] = char
    return pad, pad_map

MOVE_VECTORS: dict[ str, Vector ] = {
    "<" : Vector( -1,  0 ),
    ">" : Vector( +1,  0 ),
    "^" : Vector(  0, -1 ),
    "v" : Vector(  0, +1 ),
}
NUMPAD, NUMPAD_MAP = get_numeric_pad()
DIRPAD, DIRPAD_MAP = get_directional_pad()

def parse_data( str_data: str, verbose: bool = False ) :
    codes = str_data.strip().split( "\n" )
    print( f"Codes to enter: {codes}" )
    return codes

def is_valid_moves( start: Coordinate, moves: tuple[str], pad_map: dict[ Coordinate, str ] ) :
    position = start
    for move in moves :
        vector = MOVE_VECTORS[ move ]
        position = Coordinate( position.x + vector.dx, position.y + vector.dy )
        if position not in pad_map :
            # we are outside the pad: moves are not valid
            return False
    # we completed the moves without leaving the pad: moves are valid
    return True

@cache
def get_moves( from_key: str, to_key: str, is_numpad: bool ) :
    pad, pad_map = ( NUMPAD, NUMPAD_MAP ) if is_numpad else ( DIRPAD, DIRPAD_MAP )
    if from_key == to_key :
        # shortcut to reduce complexity: no move necessary
        return [ "A" ]
    start = pad[ from_key ]
    end = pad[ to_key ]
    move_vector = Vector( end.x - start.x, end.y - start.y )
    move_x = ">" if move_vector.dx >= 0 else "<"
    move_y = "v" if move_vector.dy >= 0 else "^"
    moves = move_x * abs( move_vector.dx ) + move_y * abs( move_vector.dy )
    valid_moves = []
    for candidate in permutations( moves ) :
        if is_valid_moves( start, candidate, pad_map ) :
            valid_moves.append( "".join( candidate ) + "A" )
    return valid_moves

@cache
def get_shortest_length( code: str, max_depth: int, cur_depth: int = 0 ) :
    current_key = "A" # starting key for all numeric & directional pads
    is_numpad = cur_depth == 0
    sequence_length = 0
    for next_key in list( code ) :
        if cur_depth == max_depth :
            # end of recursive loop
            # all sequences have the same length: we take the 1st one
            sequence_length += len( get_moves( current_key, next_key, is_numpad )[0] )
        else :
            # compute the moves on the "next" keypad to go from current to next key
            moves = get_moves( current_key, next_key, is_numpad )
            # compute the shortest length for each possible move
            sequences_length = [ get_shortest_length( move, max_depth, cur_depth + 1 )
                                for move in moves ]
            # get the minimum shortest length
            sequence_length += min( sequences_length )
        current_key = next_key
    return sequence_length

def do_problem( str_data: str, nb_directional_pads: int = 2, verbose: bool = False ) :
    codes = parse_data( str_data, verbose )
    complexity = 0
    for code in codes :
        value = int( code[0:-1] )
        length = get_shortest_length( code, nb_directional_pads )
        print( f"- {code}: sequence length = {length}" )
        complexity += value * length
    print( f"Complexity: {complexity}" )
    print( f"END" )

def do_tests( i: int = None ) :
    str_data = get_file_content( get_test_file_path( i ) )
    do_problem( str_data, 2, True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, 2, False )

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
