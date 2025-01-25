#!/usr/bin/env python3

import time
import re

def get_test_file_path() :
    return "tests.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( _file_path, _as_lines = True ) :
    with open( _file_path, 'r' ) as f :
        if ( _as_lines ) :
            data = f.readlines()
        else :
            data = f.read()
    return data

def do_check(  ) :
    None

do_dont_re = re.compile( r"(do(?:n't)?\(\))" )
mul_re = re.compile( r"mul\((\d{1,3}),(\d{1,3})\)" )

def do_part( str_data ) :
    multiplicands = mul_re.findall( str_data )
    #print( multiplicands )
    mul_result = [ int(a) * int(b) for a, b in multiplicands ]
    #print( mul_result )
    sum_mul = sum( mul_result )
    print( f"Sum of partial string: {sum_mul}" )
    return sum_mul

def do_problem( str_data ) :
    parts = do_dont_re.split( str_data )
    print( parts )
    do_mul = True
    partial_sums = []
    for part in parts :
        if part == "do()" :
            print( "Activating mul" )
            do_mul = True
        elif part == "don't()" :
            print( "Deactivating mul" )
            do_mul = False
        elif do_mul :
            print( "Mul activated: analysing partial string" )
            partial_sums.append( do_part( part ) )
        else :
            print( "Mul not activated: discarding partial string" )
    print( partial_sums )
    sum_mul = sum( partial_sums )
    print( f"Final: {sum_mul}" )

def do_tests() :
    str_data = get_file_content( get_test_file_path(), False )
    do_problem( str_data )

def do_input() :
    str_data = get_file_content( get_input_file_path(), False )
    do_problem( str_data )

def main() :
    start = time.time()
    #do_check(  )
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
