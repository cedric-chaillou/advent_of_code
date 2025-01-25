#!/usr/bin/env python3

import time

def get_test_file_path() :
    return "tests.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( _file_path, _as_lines = False ) :
    with open( _file_path, 'r' ) as f :
        if ( _as_lines ) :
            data = f.readlines()
        else :
            data = f.read()
    return data

def do_check(  ) :
    None

def get_lists( str_datas, sep = '   ' ) :
    left = []
    right = []
    for line in str_datas:
        str_values = line.split( sep )
        left.append( int( str_values[0] ) )
        right.append( int( str_values[1] ) )
    return left, right

def do_problem( left, right ) :
    left.sort()
    right.sort()
    dist = []
    for a, b in zip( left, right ) :
        d = abs( a - b )
        print( f"| {a} - {b} | = {d}" )
        dist.append( d )
    print( f"Total distance: {sum( dist )}" )

def do_tests() :
    str_datas = get_file_content( get_test_file_path(), True )
    left, right = get_lists( str_datas )
    do_problem( left, right )

def do_input() :
    str_datas = get_file_content( get_input_file_path(), True )
    left, right = get_lists( str_datas )
    do_problem( left, right )

def main() :
    start = time.time()
    #do_check( 123, 10 )
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
