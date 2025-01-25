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

def transpose_str( lines ) :
    # transformation lignes <-> colonnes
    return [ "".join(t) for t in zip( *lines ) ]

def reverse_lines( lines ) :
    # inversion des lignes texte
    return [ "".join( reversed( line ) ) for line in lines ]

def str_diagonal_tl_br( lines, row, col ) :
    str_diag = ""
    while row < len( lines ) and col < len( lines[ row ] ) :
        str_diag += lines[ row ][ col ]
        row += 1
        col += 1
    return str_diag

def diagonals_tl_br( lines, min_length = 4 ) :
    diags = []
    # diagonales qui commencent sur la 1ère colonne
    for row in range( len( lines ) ) :
        if row == 0 :
            # toutes les diagnales qui commencent sur la première ligne
            for col in range( len( lines[0] ) ) :
                diag = str_diagonal_tl_br( lines, row, col )
                if len( diag ) >= min_length :
                    diags.append( diag )
        else :
            # la diagonale qui commence sur la première colonne de la ligne
            diag = str_diagonal_tl_br( lines, row, 0 )
            if len( diag ) >= min_length :
                diags.append( diag )
    return diags

def find_in_lines( lines, searched_text, title="Found" ) :
    count = 0
    for line in lines :
        count += line.count( searched_text )
    print( f"{title}: {count}" )
    return count

def do_problem( str_data, searched_text = "XMAS" ) :
    count = 0
    # Original lines
    lines = [ line.strip() for line in str_data ]
    #print( "Lines:", lines )
    count += find_in_lines( lines, searched_text, title="Found in lines" )
    # Backwards lines
    backwards_lines = reverse_lines( lines )
    #print( "Backwards lines:", backwards_lines )
    count += find_in_lines( backwards_lines, searched_text, title="Found in backwards lines" )
    # Columns
    columns = transpose_str( lines )
    #print( "Columns:", columns )
    count += find_in_lines( columns, searched_text, title="Found in columns" )
    # Backwards columns
    columns = reverse_lines( columns ) # not necessary to keep columns
    #print( "Backwards columns:", columns )
    count += find_in_lines( columns, searched_text, title="Found in backwards columns" )
    # Diagonals top-left to bottom-right
    diagonals = diagonals_tl_br( lines )
    #print( "Diagonals top-left to bottom-right:", diagonals )
    count += find_in_lines( diagonals, searched_text, title="Found in diagonals (TL -> BR)" )
    # Diagonals bottom-right to top-left
    diagonals = reverse_lines( diagonals ) # not necessary to keep diagonals
    #print( "Diagonals bottom-right to top-left:", diagonals )
    count += find_in_lines( diagonals, searched_text, title="Found in diagonals (BR -> TL)" )
    # Diagonals top-right to bottom-left
    diagonals = diagonals_tl_br( backwards_lines ) # not necessary to keep diagonals
    #print( "Diagonals top-right to bottom-left:", diagonals )
    count += find_in_lines( diagonals, searched_text, title="Found in diagonals (TR -> BL)" )
    # Diagonals bottom-left to top-right
    diagonals = reverse_lines( diagonals ) # not necessary to keep diagonals
    #print( "Diagonals bottom-left to top-right:", diagonals )
    count += find_in_lines( diagonals, searched_text, title="Found in diagonals (BL -> TR)" )
    # Final result
    print( f"Total found (in 8 directions): {count}" )

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
