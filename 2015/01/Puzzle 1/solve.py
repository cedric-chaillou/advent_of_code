#!/usr/bin/env python3

import re

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

def compute_floor( _data ) :
    ups = len( re.findall( "\\(", _data ) )
    downs = len( re.findall( "\\)", _data ) )
    return ups - downs

def do_tests() :
    datas = get_file_content( get_test_file_path(), True )
    for data in datas :
        print( data, "=> floor #", compute_floor( data ) )

def do_input() :
    data = get_file_content( get_input_file_path(), False )
    floor_number = compute_floor( data )
    print( "Challenge result: floor #", floor_number )

def main() :
    #do_tests()
    do_input()

main()
