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

def parse_data( str_data ) :
    data = []
    for str_line in str_data :
        split_1 = str_line.split( ":", 1 )
        expected = int( split_1[0].strip() )
        operands = tuple( [ int(s) for s in split_1[1].strip().split() if s != '' ] )
        print( f"Expecting {expected} with operands {operands}" )
        data.append( ( expected, operands ) )
    return data

def mul( a, b ) :
    return a * b

def add( a, b ) :
    return a + b

def concat( a, b ) :
    return int( str(a) + str(b) )

OPERATORS = ( mul, add, concat )

def str_base( number, base = "01" ) :
    q, r = divmod( number, len( base ) )
    if q > 0 :
        return str_base( q, base ) + base[ r ]
    else :
        return base[ r ]

def sequence_base( number, base = OPERATORS, type = tuple ) :
    q, r = divmod( number, len( base ) )
    if q > 0 :
        return sequence_base( q, base, type ) + type( [ base[ r ] ] )
    else :
        return type( [ base[ r ] ] )

def compute( operands, operators ) :
    result = operands[0]
    for operand, operator in zip( operands[1:], operators ) :
        result = operator( result, operand )
    return result

def find_operators( expected, operands ) :
    nb_operators = len( operands ) - 1
    print( f"Searching {nb_operators} operators to get {expected} from operands {operands} ..." )
    operators_found = []
    if nb_operators == 0 :
        if operands[0] == expected :
            operators_found.append( tuple() )
    else :
        nb_tests = pow( len( OPERATORS ), nb_operators )
        #print( f"Nb combinations to test: {nb_tests}" )
        for number in range( nb_tests ) :
            operators = sequence_base( number, OPERATORS, tuple )
            if ( len(operators) < nb_operators ) :
                # we "left pad" the tuple with the operation corresponding to number 0
                nb_needed = nb_operators - len(operators)
                operators = ( OPERATORS[0], ) * nb_needed + operators
            #print( f"{number} => {operators}" )
            result = compute( operands, operators )
            if ( result == expected ) :
                print( "SUCCESS: Operators found:", operators )
                operators_found.append( operators )
    if len( operators_found ) == 0 :
        print( "FAILURE: No operators combination found" )
    return operators_found

def do_problem( str_data ) :
    data = parse_data( str_data )
    final_sum = 0
    for expected, operands in data :
        if len( find_operators( expected, operands ) ) > 0 :
            final_sum += expected
    print( "Final sum:", final_sum )

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
