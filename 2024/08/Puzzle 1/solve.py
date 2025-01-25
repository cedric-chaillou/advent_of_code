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
    row_1, col_1 = antenna_1
    row_2, col_2 = antenna_2
    vector_1_to_2 = ( row_2 - row_1, col_2 - col_1 ) # vector to go from antenna 1 to 2
    # 1er antinode : à l'opposé de antenna_1 en partant de antenna_2
    antinode_1 = tuple( c + v for c, v in zip( antenna_2, vector_1_to_2 ) )
    if is_in_grid( grid, antinode_1 ) :
        antinodes.add( antinode_1 )
    # 2e antinode : à l'opposé de antenna_2 en partant de antenna_1
    antinode_2 = tuple( c - v for c, v in zip( antenna_1, vector_1_to_2 ) )
    if is_in_grid( grid, antinode_2 ) :
        antinodes.add( antinode_2 )
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
