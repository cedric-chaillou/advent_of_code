#!/usr/bin/env python3

import time
from itertools import combinations

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

EMPTY = "."

def parse_data( str_data, print_data = False ) :
    disk = []
    next_file_id = 0
    next_is_file = True
    for digit in list( str_data.strip() ) :
        if next_is_file :
            disk += [ next_file_id, ] * int( digit )
            next_file_id += 1
        else :
            disk += [ None, ] * int( digit )
        next_is_file = not next_is_file
    print( f"Disk size: {len(disk)}" )
    print( f"Nb files: {next_file_id}" )
    if print_data :
        print_disk( disk, next_file_id )
    return disk, next_file_id

def print_disk( disk, nb_files ) :
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    empty = "."
    if nb_files > len(chars) :
        print( f"WARNING: not enough chars ({len(chars)}) to represents {nb_files} files!" )
    str_disk = ""
    for id in disk :
        if id is None :
            str_disk += empty
        else :
            str_disk += chars[ id % len(chars) ]
    print( str_disk )

def fragment_disk( disk, nb_files, print_steps = False ) :
    if None in disk :
        curser_free = disk.index( None )
        curser_frag = len( disk ) - 1
        while curser_frag > curser_free :
            if disk[ curser_frag ] is not None :
                disk[ curser_free ] = disk[ curser_frag ]
                disk[ curser_frag ] = None
                if print_steps :
                    print_disk( disk, nb_files )
                curser_free = disk.index( None )
            curser_frag -= 1
    return disk

def get_checksum( disk ) :
    checksum = 0
    for sector_id, file_id in enumerate( disk ) :
        if file_id is None :
            break
        checksum += sector_id * file_id
    return checksum

def do_problem( str_data ) :
    disk, nb_files = parse_data( str_data, True )
    fragment_disk( disk, nb_files, True )
    print( "Final disk setup:" )
    print_disk( disk, nb_files )
    print( "Final disk checksum:", get_checksum( disk ) )

def do_tests() :
    str_data = get_file_content( get_test_file_path(), False )
    do_problem( str_data )

def do_input() :
    str_data = get_file_content( get_input_file_path(), False )
    do_problem( str_data )

def main() :
    start = time.time()
    #do_check(  )
    do_tests()
    #do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
