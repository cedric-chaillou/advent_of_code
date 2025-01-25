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

def parse_data( str_data ) :
    files = []
    free = []
    index = 0
    file_id = 0
    next_is_file = True
    for digit in list( str_data.strip() ) :
        nb_sectors = int( digit )
        if next_is_file :
            files.append( ( file_id, index, nb_sectors ) )
            file_id += 1
        elif nb_sectors != 0 :
            free.append( ( index, nb_sectors ) )
        index += nb_sectors
        next_is_file = not next_is_file
    return files, free

def get_disk( files, free ) :
    disk = files + [ ( None, address, size ) for address, size in free ]
    disk.sort( key = lambda t : t[1] ) # sort by address (2nd element in tuple)
    return disk

def print_files_free( files, free, list_files = False, list_free = False ) :
    occupied  = sum( [ size for id, address, size in files ] )
    free_size  = sum( [ size for address, size in free ] )
    print( f"Disk size: {occupied+free_size}" )
    print( f"    {len(files)} file(s) occupying {occupied} sectors" )
    print( f"    {len(free)} free slots occupying {free_size} sectors" )
    if list_files :
        print( "Files list:" )
        for id, address, size in files :
            print( f"    @{address} ({size} sectors): file #{id}" )
    if list_files :
        print( "Free slots:" )
        for address, size in free :
            print( f"    @{address} ({size} sectors) ")


def print_disk( disk, nb_files ) :
    chars = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ²&~éàèìòùäëïöüñãõ"#'{}()[]-|`_\ç^@=¨$£%*µ<>,?;:/!§"""
    empty = "."
    if nb_files > len(chars) :
        print( f"WARNING: not enough chars ({len(chars)}) to represents {nb_files} files!" )
    str_disk = ""
    for id, address, size in disk :
        if id is None :
            str_disk += empty * size
        else :
            str_disk += chars[ id % len(chars) ] * size
    print( str_disk )

def compact_free( free ) :
    print( f"Compacting {len(free)} free slots ..." )
    free.sort( key = lambda t : t[0] ) # sort by address (1st element in tuple)
    new_free = []
    last_address, last_size = -1, 0
    for address, size in free :
        if size == 0 :
            # remove 0-size free slots
            print( f"Free slot @{address} ({size} sectors): delete" )
        elif address == last_address + last_size :
            # merge contiguous free slots
            print( f"Free slot @{address} ({size} sectors): merge with @{last_address} ({last_size} sectors)" )
            last_size += size
            new_free[ len(new_free) - 1 ] = ( last_address, last_size )
        else :
            # keep free slot "as is"
            last_address, last_size = address, size
            new_free.append( ( last_address, last_size ) )
    print( f"Free slots compacted to {len(new_free)} slots" )
    return new_free

def move_files( files, free ) :
    for idx_file in reversed( range( len( files ) ) ) :
        file_id, file_address, file_size = files[ idx_file ]
        for idx_free, free_slot in enumerate( free ) :
            free_address, free_size = free_slot
            if free_address >= file_address :
                # we don't move a file towards the end of the disk : stop loop here
                print( f"File #{file_id} ({file_size} sectors) not moved: no free slot found" )
                break
            if file_size <= free_size :
                print( f"File #{file_id} ({file_size} sectors) moved from @{file_address} to @{free_address}" )
                # move the file
                files[ idx_file ] = ( file_id, free_address, file_size )
                # modify the slot used
                new_free_address = free_address + file_size
                new_free_size = free_size - file_size
                print( f"Free slot @{free_address} ({free_size} sectors) => free slot @{new_free_address} ({new_free_size} sectors)" )
                free[ idx_free ] = ( new_free_address, new_free_size )
                # add free slot where the file was
                print( f"New free slot @{file_address} ({file_size} sectors)" )
                free.append( ( file_address, file_size ) )
                free = compact_free( free )
                break
    files.sort( key = lambda t : t[1] ) # sort by address (2nd element in tuple)
    return files, free

def get_checksum( files ) :
    checksum = 0
    for id, address, size in files :
        for sub_address in range( size ) :
            checksum += id * ( address + sub_address )
    return checksum

def do_problem( str_data, verbose = False ) :
    files, free = parse_data( str_data )
    print( "Initial disk setup:" )
    print_files_free( files, free, verbose, verbose )
    if verbose :
        print_disk( get_disk( files, free ), len(files) )
    files, free = move_files( files, free )
    print( "Final disk setup:" )
    print_files_free( files, free, verbose, verbose )
    if verbose :
        print_disk( get_disk( files, free ), len(files) )
    print( "Final disk checksum:", get_checksum( files ))

def do_tests() :
    str_data = get_file_content( get_test_file_path(), False )
    do_problem( str_data, True )

def do_input() :
    str_data = get_file_content( get_input_file_path(), False )
    do_problem( str_data, False )

def main() :
    start = time.time()
    #do_check(  )
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
