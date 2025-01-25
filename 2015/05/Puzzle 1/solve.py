#!/usr/bin/env python3

import time
from functools import partial

def get_test_file_path( i = None ) :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

def parse_data( str_data: str, verbose: bool = False ) :
    return str_data.strip().split( "\n" )

def contains( string: str, sub_strings: tuple[str], min_occurs: int=1, inverse: bool=False ) -> bool:
    nb_hits = 0
    for sub in sub_strings :
        nb_hits += string.count( sub )
        if nb_hits >= min_occurs :
            return not inverse
    return inverse

def repeat( string: str, length_sub: int=1, nb_repeats: int=2, inverse: bool=False ) :
    length_test = length_sub * nb_repeats
    for i in range( len(string) - length_test + 1 ) :
        sub = string[i:i+length_sub]
        test = string[i:i+length_test]
        if test == sub * nb_repeats :
            return not inverse
    return inverse

RULES = (
    partial( contains, sub_strings=( 'a', 'e', 'i', 'o', 'u' ), min_occurs=3, inverse=False ),
    partial( repeat, length_sub=1, nb_repeats=2, inverse=False ),
    partial( contains, sub_strings=( 'ab', 'cd', 'pq', 'xy' ), min_occurs=1, inverse=True )
    )

def is_nice( string: str, verbose: bool ) -> int :
    if verbose :
        print( f"Testing string '{string}'..." )
    for i, rule in enumerate( RULES, start=1 ) :
        if not rule( string = string ) :
            if verbose :
                print( f"{string} is naughty, fails rule #{i}" )
            return 0
    if verbose :
        print( f"{string} is nice" )
    return 1

def do_problem( str_data: str, verbose = False ) :
    strings = parse_data( str_data, verbose )
    print( f"{len(strings)} strings to test..." )
    nice = 0
    for string in strings :
        nice += is_nice( string, verbose )
    print( f"{nice} nice strings" )
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
