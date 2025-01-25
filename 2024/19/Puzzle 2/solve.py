#!/usr/bin/env python3

import time
from functools import cache

def get_test_file_path( i = None ) :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    print( f"Reading file {file_path}" )
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

def parse_data( str_data: str, verbose: bool = False ) :
    lines = str_data.split( "\n" )
    towel_patterns = tuple( lines[0].split( ", " ) )
    designs = lines[2:]
    if verbose :
        print( f"Avalaible towel patterns: {', '.join(towel_patterns)}" )
        print( f"Wanted designs: {', '.join(designs)}" )
    print( f"Nb of available towel patterns: {len(towel_patterns)}" )
    print( f"Nb of wanted designs: {len(designs)}" )
    print()
    return towel_patterns, designs

@cache
def design_possible( design: str, towel_patterns: tuple[str], verbose: bool = False ) -> bool :
    if verbose :
        print( f"Solving for design: {design}" )
    if design == "" :
        # end of recursive loop!
        return True
    for pattern in towel_patterns :
        if design[:len(pattern)] == pattern :
            # the start of the design match the pattern
            # recursive call to see if the rest of the design is possible
            if design_possible( design[len(pattern):], towel_patterns, verbose ) :
                # if yes, we return True immediatly to stop the search
                return True
            # otherwise, we check with the next pattern
        # otherwise, we check with the next pattern
    return False

@cache
def nb_arrangements( design: str, towel_patterns: tuple[str], verbose: bool = False ) -> int :
    if verbose :
        print( f"Solving for design: {design}" )
    if design == "" :
        # end of recursive loop!
        return 1
    count = 0 # nb of possible arrangements for the design
    for pattern in towel_patterns :
        if design[:len(pattern)] == pattern :
            # the start of the design match the pattern
            # recursive call to get the nb of arrangements for the rest of the design
            count += nb_arrangements( design[len(pattern):], towel_patterns, verbose )
        # otherwise, we check with the next pattern
    return count

def do_problem( str_data: str, verbose = False ) :
    towel_patterns, designs = parse_data( str_data, verbose )
    possible = [ nb_arrangements( d, towel_patterns, verbose ) for d in designs ]
    if verbose :
        print( f"Arrangemens found: {', '.join( [ str(c) for c in possible ] )}" )
    print( f"Nb of arrangemens found: {sum(possible)}" )
    print( f"END" )

def do_tests( i = None ) :
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
