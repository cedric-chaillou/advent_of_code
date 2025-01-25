#!/usr/bin/env python3

import re

def get_test_file_path() :
    return "tests.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( _file_path, _as_lines = False ) :
    with open( _file_path, 'r' ) as f :
        if ( _as_lines ) :
            data = [ line.rstrip() for line in f ]
        else :
            data = f.read()
    return data

def find_floor( _data, _stop_at_floor = 0 ) :
    if ( _stop_at_floor == 0 ) :
        return 0
    floor = 0
    floor_found = False
    for p, c in enumerate( _data ) :
        if c == "(" :
            floor += 1
        elif c == ")" :
            floor -= 1
        floor_found = ( floor == _stop_at_floor )
        if floor_found :
            break
    return ( p + 1 ) if floor_found else None

def do_tests() :
    datas = get_file_content( get_test_file_path(), True )
    for data in datas :
        print( data, "=> basement reached at position #", find_floor( data, -1 ) )

def do_input() :
    data = get_file_content( get_input_file_path(), False )
    position_basement = find_floor( data, -1 )
    print( "Challenge result: basement reached at position #", position_basement )

def main() :
    do_tests()
    do_input()

if __name__ == '__main__':
    main()
