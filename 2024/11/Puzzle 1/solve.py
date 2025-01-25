#!/usr/bin/env python3

import time
from itertools import combinations

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

def parse_data( str_data ) :
    stones = [ int( s ) for s in str_data.strip().split() ]
    return stones

def blink_stone( stone ) :
    if stone == 0 :
        return [ 1, ]
    str_stone = str( stone )
    nb_digits = len( str_stone )
    if nb_digits % 2 == 0 :
        half_length = nb_digits // 2
        return [ int( str_stone[:half_length] ), int( str_stone[half_length:] ) ]
    return [ stone * 2024, ]

def blink_stones( stones, iteration, print_for_nb_stones = 25 ) :
    new_stones = []
    for stone in stones :
        new_stones += blink_stone( stone )
    if len( new_stones ) < print_for_nb_stones :
        print( f"After {iteration} blink(s), stones: {new_stones}" )
    print( f"After {iteration} blink(s), number of stones: {len(new_stones)}" )
    return new_stones

def do_problem( str_data, nb_blinks = 25 ) :
    stones = parse_data( str_data )
    print( f"Initial stones: {stones}" )
    print( f"Initial number of stones: {len(stones)}" )
    for i in range( nb_blinks ) :
        stones = blink_stones( stones, i+1 )
    print( f"Final number of stones: {len(stones)}" )

def do_tests() :
    str_data = get_file_content( get_test_file_path(), False )
    do_problem( str_data )

def do_input() :
    str_data = get_file_content( get_input_file_path(), False )
    do_problem( str_data )

def main() :
    start = time.time()
    #do_check(  )
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
