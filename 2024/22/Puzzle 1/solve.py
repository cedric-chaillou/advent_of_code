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

def mix( a, b ) :
    return a ^ b

def prune( a ) :
    # 16777216 = 0x1000000 = 0xffffff + 1
    # donc a % 16777216 == a & 0xffffff
    return a & 0xffffff

def mul_bin( a, b ) :
    # a * 2^b
    return a << b

def mul_2048( a ) :
    return mul_bin( a, 11 )

def mul_64( a ) :
    return mul_bin( a, 6 )

def div_int_bin( a, b ) :
    # a / 2^b, rounded down
    return a >> b

def div_32( a ) :
    return div_int_bin( a, 5 )

def next_secret_number( secret_number ) :
    secret_number = prune( mix( mul_64( secret_number ), secret_number ) )
    secret_number = prune( mix( div_32( secret_number ), secret_number ) )
    secret_number = prune( mix( mul_2048( secret_number ), secret_number ) )
    return secret_number

def iter_secret_number( secret_number, nb_iter = 2000 ) :
    for i in range( nb_iter ) :
        secret_number = next_secret_number( secret_number )
    return secret_number

def do_check( secret_number, nb_iter ) :
    print( f"Start: {secret_number}" )
    for i in range( nb_iter ) :
        print( f"{i}: {secret_number}" )
        secret_number = next_secret_number( secret_number )
    print( f"{nb_iter}: {secret_number}" )

def do_tests() :
    datas = get_file_content( get_test_file_path(), True )
    tests = [ int( x.strip() ) for x in datas ]
    results = [ iter_secret_number( x ) for x in tests ]
    print( sum( results ) )

def do_input() :
    datas = get_file_content( get_input_file_path(), True )
    tests = [ int( x.strip() ) for x in datas ]
    results = [ iter_secret_number( x ) for x in tests ]
    print( sum( results ) )

def main() :
    #do_check( 123, 10 )
    #do_tests()
    do_input()

main()
