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
    pages_after = {} # pour chaque page, on donne la liste des pages qui doivent être après
    pages_before = {} # pour chaque page, on donne la liste des pages qui doivent être avant
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
    return pages_before, page_sequences

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

def check_sequence( pages_before, sequence, fix = False ) :
    is_valid = True
    valid_start_sequence = sequence
    remaining_sequence = []
    next_expected_page = None
    for j, page in enumerate( sequence ) :
        # checking that the next sequence don't contain a page that should be BEFORE this page number
        if page in pages_before :
            x = first_intersect( sequence[j+1:], pages_before[ page ] )
            if x is not None :
                print( f"{sequence} is an INVALID page sequence: {x} should be BEFORE {page}" )
                is_valid = False
                valid_start_sequence = sequence[:j]
                remaining_sequence = sequence[j:]
                next_expected_page = x
                break
    if is_valid :
        print( f"{sequence} is a VALID page sequence" )
    if fix :
        return is_valid, valid_start_sequence, remaining_sequence, next_expected_page
    else :
        return is_valid

def get_invalid_sequences( pages_before, page_sequences ) :
    invalid_sequences = []
    print()
    print( "Checking page sequences" )
    count_valid = 0
    sum_middle_page = 0
    for sequence in page_sequences :
        if check_sequence( pages_before, sequence ) :
            count_valid += 1
            sum_middle_page += get_median( sequence )
        else :
            invalid_sequences.append( sequence )
    print( f"{count_valid} valid sequences found out of {len(page_sequences)}" )
    print( f"Sum of middle page numbers: {sum_middle_page}" )
    return invalid_sequences

def fix_sequence( pages_before, sequence ) :
    is_valid, valid_start_sequence, remaining_sequence, next_expected_page = check_sequence( pages_before, sequence, fix=True )
    valid_sequence = valid_start_sequence
    while not is_valid :
        end_sequence = []
        while next_expected_page in remaining_sequence :
            end_sequence.append( remaining_sequence.pop( remaining_sequence.index( next_expected_page ) ) )
        end_sequence += remaining_sequence
        is_valid, valid_start_sequence, remaining_sequence, next_expected_page = check_sequence( pages_before, end_sequence, fix=True )
        valid_sequence += valid_start_sequence
    return valid_sequence

def do_problem( str_data ) :
    pages_before, page_sequences = parse_data( str_data )
    invalid_sequences = get_invalid_sequences( pages_before, page_sequences )
    print()
    print( f"{len(invalid_sequences)} invalid sequences to fix..." )
    fixed_sequences = []
    for sequence in invalid_sequences :
        print( f"Invalid sequence {sequence}" )
        fixed_sequence = fix_sequence( pages_before, sequence )
        print( f"=> VALID sequence {fixed_sequence}" )
        fixed_sequences.append( fixed_sequence )
    print()
    print( "Check and middle value sum..." )
    invalid_sequences = get_invalid_sequences( pages_before, fixed_sequences )
    if len( invalid_sequences ) == 0 :
        print( "ALL DONE!" )
    else :
        print( f"ERROR! {len(invalid_sequences)} INVALID SEQUENCES REMAINING..." )
        for s in invalid_sequences :
            print( s )

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
