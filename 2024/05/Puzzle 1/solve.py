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

order_re = re.compile( r"^(\d+)\|(\d+)$" )
pages_re = re.compile( r"^\d+(?:,\d+)*$" )

def parse_data( lines ) :
    print( "Parsing input data..." )
    pages_after = {} # pour chaque page, on donne la liste des sequence qu'elle précède
    pages_before = {} # pour chaque page, on donne la liste des sequence qu'elle suit
    page_sequences = []
    for line in lines :
        line = line.strip()
        if line == "" :
            print( "Empty line" )
            continue
        m_order = order_re.fullmatch( line )
        if m_order is not None :
            page_before = int( m_order[1] )
            page_after = int( m_order[2] )
            print( f"Ordering instruction: {page_before} before {page_after}" )
            if page_before in pages_after :
                pages_after[ page_before ].append( page_after )
            else :
                pages_after[ page_before ] = [ page_after, ]
            if page_after in pages_before :
                pages_before[ page_after ].append( page_before )
            else :
                pages_before[ page_after ] = [ page_before, ]
            continue
        m_page = pages_re.fullmatch( line )
        if m_page is not None :
            sequence = [ int( p ) for p in line.split( "," ) ]
            print( f"Page sequence : {sequence}" )
            page_sequences.append( sequence )
            continue
    #print( "Pages after key page:", pages_after )
    #print( "Pages before key page:", pages_before )
    #print( "Page lists:", page_sequences )
    return pages_after, pages_before, page_sequences

def first_intersect( list_a, list_b ) :
    for a in list_a :
        if a in list_b :
            return a
    return None

def get_median( numbers ) :
    if len( numbers ) == 0 :
        return 0
    if len( numbers ) % 2 == 1 :
        return numbers[ ( len( numbers ) - 1 ) // 2 ]
    else :
        a = numbers[ ( len( numbers ) - 2 ) // 2 ]
        b = numbers[ len( numbers ) // 2 ]
        return ( a + b ) / 2

def do_problem( str_data ) :
    pages_after, pages_before, page_sequences = parse_data( str_data )
    print()
    print( "Checking page sequences" )
    count_valid = 0
    sum_middle_page = 0
    for i, sequence in enumerate( page_sequences ) :
        is_valid = True
        for j, page in enumerate( sequence ) :
            # checking that the next sequence don't contain a page that should be BEFORE this page number
            if page in pages_before :
                x = first_intersect( sequence[j+1:], pages_before[ page ] )
                if x is not None :
                    print( f"{sequence} is an INVALID page sequence: {x} should be BEFORE {page}" )
                    is_valid = False
                    break
        if is_valid :
            print( f"{sequence} is a VALID page sequence" )
            count_valid += 1
            sum_middle_page += get_median( sequence )
    print( f"{count_valid} valid sequences found out of {len(page_sequences)}" )
    print( f"Sum of middle page numbers: {sum_middle_page}" )

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
