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

def find_cliques( network: dict[ str, set[str] ], verbose: bool = False ) :
    cliques = set()
    
    # BRON-KERBOSCH ALGORITHM
    # https://en.wikipedia.org/wiki/Bron–Kerbosch_algorithm
    # https://fr.wikipedia.org/wiki/Algorithme_de_Bron-Kerbosch
    def bron_kerbosch( r: set[str], p: set[str], x: set[str] ) :
        if len(p) == 0 and len(x) == 0 :
            new_clique = tuple( sorted( r ) )
            if verbose :
                print( f"Adding {len(new_clique)}-computers clique; {new_clique}" )
            cliques.add( new_clique )
        else :
            p_tuple = tuple( sorted( p ) )
            for node in p_tuple :
                new_r = r.union( { node } )
                new_p = p.intersection( network[ node ] )
                new_x = x.intersection( network[ node ] )
                bron_kerbosch( new_r, new_p, new_x )
                p.remove( node )
                x.add( node )

    # initial call
    print( f"Searching for cliques..." )
    bron_kerbosch( set(), set( network.keys() ), set() )
    print( f"{len(cliques)} cliques found" )
    return cliques

def do_problem( str_data: str, verbose: bool = False ) :
    network = parse_data( str_data, verbose )
    cliques = find_cliques( network, verbose )
    max_clique = max( cliques, key = len )
    print( f"Maximum sized clique contains {len(max_clique)} computers:" )
    clique_signature = ",".join( max_clique )
    print( f"\n{clique_signature}\n" )
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
