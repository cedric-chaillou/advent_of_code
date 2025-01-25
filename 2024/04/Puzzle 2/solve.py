#!/usr/bin/env python3

import time

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

def is_x_mas( lines, row, col, word ) :
    backwards = "".join( reversed( word ) ) # "SAM"
    center = word[ 1 ] # "A"
    top_left = lines[ row - 1 ][ col - 1 ]
    top_right = lines[ row - 1 ][ col + 1 ]
    bottom_left = lines[ row + 1 ][ col - 1 ]
    bottom_right = lines[ row + 1 ][ col + 1 ]
    word1 = "".join( [ top_left, center, bottom_right ] )
    word2 = "".join( [ top_right, center, bottom_left ] )
    return ( word1 == word or word1 == backwards ) and ( word2 == word or word2 == backwards )

def do_problem( str_data, word = "MAS" ) :
    count = 0
    center = word[ 1 ] # "A"
    lines = [ line.strip() for line in str_data ]
    for row in range( 1, len( lines ) - 1 ) :
        for col in range( 1, len( lines[ row ] ) - 1 ) :
            if lines[ row ][ col ] == center :
                if is_x_mas( lines, row, col, word ) :
                    count += 1
    print( f"Total X-MAS found: {count}" )

def do_tests() :
    str_data = get_file_content( get_test_file_path(), True )
    do_problem( str_data )

def do_input() :
    str_data = get_file_content( get_input_file_path(), True )
    do_problem( str_data )

def main() :
    start = time.time()
    #do_check(  )
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
