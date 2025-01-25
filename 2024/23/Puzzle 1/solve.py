#!/usr/bin/env python3

import time
from collections import namedtuple
import re

def get_test_file_path( i: int = None ) -> str :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() -> str :
    return "input.txt"

def get_file_content( file_path: str ) -> str :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

def parse_data( str_data: str, verbose: bool = False ) :
    network: dict[ str, set[str] ] = dict()
    for line in str_data.strip().split( "\n" ) :
        comp1, comp2 = tuple( line.split( "-", 1 ) )
        if comp1 not in network :
            network[ comp1 ] = set()
        if comp2 not in network :
            network[ comp2 ] = set()
        network[ comp1 ].add( comp2 )
        network[ comp2 ].add( comp1 )
    if verbose :
        for comp in network :
            print( f"Connected to {comp}: {network[ comp ]}" )
    return network

def find_sets( network: dict[ str, set[str] ], filter: str = None, verbose: bool = False ) :
    comp_sets = set()
    for comp1 in network :
        for comp2 in network[ comp1 ] :
            comp3_set = network[ comp1 ].intersection( network[ comp2 ] )
            for comp3 in comp3_set :
                if filter is None or comp1[0] == filter or comp2[0] == filter or comp3[0] == filter :
                    comp_sets.add( tuple( sorted( [ comp1, comp2, comp3 ] ) ) )
    if verbose :
        for comp_set in comp_sets :
            print( f"Computer set: {comp_set}" )
    return comp_sets

def do_problem( str_data: str, verbose: bool = False ) :
    network = parse_data( str_data, verbose )
    #print()
    #print( "All sets of 3" )
    #comp_sets = find_sets( network, None, verbose )
    print()
    print( "All sets of 3 starting wth 't'" )
    t_comp_sets = find_sets( network, "t", verbose )
    print()
    print( f"Nb of sets of 3 starting wth 't': {len(t_comp_sets)}" )
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
