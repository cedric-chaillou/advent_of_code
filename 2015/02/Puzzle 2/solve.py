#!/usr/bin/env python3

import time
import re

def get_test_file_path( i = None ) :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

BOX_RE = re.compile( r"(\d+)x(\d+)x(\d+)" )

def parse_data( str_data: str, verbose: bool = False ) :
    boxes = []
    for line in str_data.strip().split( "\n" ) :
        match = BOX_RE.match( line )
        if match is not None :
            boxes.append( tuple( int(v) for v in match.groups() ) )
    print( f"{len(boxes)} boxes read" )
    return boxes

def get_ribbon_length( l, w, h ) :
    half_perimeters = [ l+w, l+h, w+h ]
    return 2 * min(half_perimeters) + l*w*h

def get_paper_surface( l, w, h ) :
    sides = [ l*w, l*h, w*h ]
    return 2 * sum(sides) + min(sides)

def do_problem( str_data: str, verbose = False ) :
    boxes = parse_data( str_data, verbose )
    total_paper = 0
    total_ribbon = 0
    for box in boxes :
        box_paper = get_paper_surface( *box )
        box_ribbon = get_ribbon_length( *box )
        if verbose :
            print( f"Box {box} needs {box_paper} square feet of paper and {box_ribbon} feet of ribbon" )
        total_paper += box_paper
        total_ribbon += box_ribbon
    print( f"Total square feet of paper needed: {total_paper}" )
    print( f"Total feet of ribbon needed: {total_ribbon}" )
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
