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

EMPTY = "."

def parse_data( str_data, print_grid = False ) :
    grid = [] # map
    frequencies = {} # key = frequency, value = list of antenna coordinates
    for row, line in enumerate( str_data ) :
        tiles = list( line.strip() )
        grid.append( tiles )
        for col, tile in enumerate( tiles ) :
            if tile != EMPTY :
                if tile in frequencies :
                    frequencies[ tile ].append( ( row, col ) )
                else :
                    frequencies[ tile ] = [ ( row, col ), ]
    if print_grid :
        for line in grid :
            print( "".join( line ) )
    print( f"Grid size: {len(grid)}x{len(grid[0])}" )
    print( f"Frequencies:" )
    for f in frequencies :
        print( f"- {f}, {len(frequencies[f])} antenna(s): {frequencies[f]}" )
    return grid, frequencies

def is_in_grid( grid, position ) :
    row, col = position
    if row < 0 or col < 0 :
        return False
    if row >= len( grid ) :
        return False
    if col >= len( grid[ row ] ) :
        return False
    return True

def antennas_antinodes( grid, antenna_1, antenna_2 ) :
    #print( f"Calculating antinodes between antennas {antenna_1} and {antenna_2}" )
    antinodes = set()
    vector = tuple( [ c2-c1 for c1, c2 in zip( antenna_1, antenna_2 ) ] ) # vector to go from antenna 1 to 2
    # antinodes starting from antenna_2, away from antenna_1
    antinode = antenna_2
    while is_in_grid( grid, antinode ) :
        antinodes.add( antinode )
        antinode = tuple( c+v for c, v in zip( antinode, vector ) )
    # antinodes starting from antenna_1, away from antenna_2
    antinode = antenna_1
    while is_in_grid( grid, antinode ) :
        antinodes.add( antinode )
        antinode = tuple( c-v for c, v in zip( antinode, vector ) )
    print( f"Antinodes between antennas {antenna_1} and {antenna_2}: {len(antinodes)}" )
    return antinodes

def frequency_antinodes( grid, antennas, frequency ) :
    print( f"Calculating antinodes for frequency {frequency}" )
    antinodes = set()
    for antenna_1, antenna_2 in combinations( antennas, 2 ) :
        antinodes = antinodes | antennas_antinodes( grid, antenna_1, antenna_2 )
    print( f"Antinodes for frequency {frequency}: {len(antinodes)}" )
    return antinodes

def do_problem( str_data ) :
    grid, frequencies = parse_data( str_data, True )
    antinodes = set()
    for f in frequencies :
        antinodes = antinodes | frequency_antinodes( grid, frequencies[ f ], f )
    print( f"Total number of antinodes: {len(antinodes)}" )

def do_tests() :
    str_data = get_file_content( get_test_file_path(), True )
    do_problem( str_data )

def do_input() :
    str_data = get_file_content( get_input_file_path(), True )
    do_problem( str_data )

def main() :
    start = time.time()
    #do_check(  )
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
