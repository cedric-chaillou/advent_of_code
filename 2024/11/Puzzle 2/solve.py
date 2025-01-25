#!/usr/bin/env python3

import time
from functools import cache

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

@cache
def blink_stone( stone, iteration = 0, max_iteration = 25 ) :
    if iteration == max_iteration :
        return 1 # 1 stone
    if stone == 0 :
        return blink_stone( 1, iteration + 1, max_iteration )
    str_stone = str( stone )
    nb_digits = len( str_stone )
    if nb_digits % 2 == 0 :
        middle = nb_digits // 2
        left = int( str_stone[:middle] )
        right = int( str_stone[middle:] )
        return blink_stone( left, iteration + 1, max_iteration ) + blink_stone( right, iteration + 1, max_iteration )
    return blink_stone( stone * 2024, iteration + 1, max_iteration )

def do_problem( str_data ) :
    stones = parse_data( str_data )
    print( f"Initial stones: {stones}" )
    print( f"Initial number of stones: {len(stones)}" )
    nb_stones = 0
    for stone in stones :
        nb_stones += blink_stone( stone, max_iteration = 75 )
    print( f"Final number of stones: {nb_stones}" )

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
