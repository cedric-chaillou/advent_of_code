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

def parse_data( str_datas, sep = ' ' ) :
    all_datas = []
    for str_line in str_datas:
        line_data = [ int(s) for s in str_line.split( sep ) ]
        all_datas.append( line_data )
    return all_datas

def check_report( report, min_diff = 1, max_diff = 3 ) :
    safe = True
    prev_diff = 0
    prev = report[0]
    for v in report[1:] :
        diff = v - prev
        if abs( diff ) < min_diff :
            #print( f"Difference {diff} < {min_diff}" )
            safe = False
            break
        if abs( diff ) > max_diff :
            #print( f"Difference {diff} > {max_diff}" )
            safe = False
            break
        prev = v
        if diff != 0 :
            if prev_diff * diff < 0 :
                #print( f"Change of direction from {prev_diff} to {diff}" )
                safe = False
                break
            prev_diff = diff
    return safe

def do_problem( data ) :
    all_results = []
    for i, line in enumerate( data ) :
        safe = check_report( line )
        print( f"{i+1}: {'Safe' if safe else 'Unsafe'}" )
        all_results.append( 1 if safe else 0 )
    print( f"Number of safe reports found: {sum( all_results )}" )

def do_tests() :
    str_datas = get_file_content( get_test_file_path(), True )
    data = parse_data( str_datas )
    do_problem( data )

def do_input() :
    str_datas = get_file_content( get_input_file_path(), True )
    data = parse_data( str_datas )
    do_problem( data )

def main() :
    start = time.time()
    #do_check(  )
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
