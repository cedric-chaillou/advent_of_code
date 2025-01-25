#!/usr/bin/env python3

import time
from hashlib import md5

def get_test_file_path( i = None ) :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

def parse_data( str_data: str, verbose: bool = False ) :
    return str_data.strip()

def hash_starts_with( key: str, number: int, searched: str ) -> bool :
    text = key + str(number)
    hash = md5( text.encode('ascii') ).hexdigest()
    return hash[:len(searched)] == searched

def solve( key: str, searched: str ) :
    number = 0
    while not hash_starts_with( key, number, searched ) :
        number += 1
    return number

def do_problem( str_data: str, verbose = False ) :
    key = parse_data( str_data, verbose )
    number = solve( key, "0" * 5 )
    print( f"Number found: {number}" )
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
