#!/usr/bin/env python3

import time
from functools import cache

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

START = 0
END = 9
NEXT = 1
TILES = {}

def add_neighbour( tile, neighbour ) :
    if neighbour[ "height" ] - tile[ "height" ] == NEXT :
        # we can hike from tile to neighbour
        tile[ "next" ].append( neighbour[ "coords" ] )
    elif tile[ "height" ] - neighbour[ "height" ] == NEXT :
        # we can hike from neighbour to tile
        neighbour[ "next" ].append( tile[ "coords" ] )

def parse_data( str_data, verbose = False ) :
    tiles = {}
    start = []
    nb_rows = len( str_data )
    for row, line in enumerate( [ l.strip() for l in str_data ] ) :
        if row == 0 :
            nb_cols = len( line )
        if verbose :
            print( f"Row {row}: {line}" )
        for col, height in enumerate( [ int(h) for h in list( line ) ] ) :
            coords = ( row, col )
            #print( f"Coords: {coords}, height: {height}" )
            tile = {
                "coords" : coords,
                "height" : height,
                "next" : [],
            }
            if row > 0 :
                add_neighbour( tile, tiles[ ( row - 1, col ) ] )
            if col > 0 :
                add_neighbour( tile, tiles[ ( row, col - 1 ) ] )
            tiles[ coords ] = tile
            #print( f"List of tiles: {tiles.keys()}" )
            if height == START :
                start.append( coords )
    print( f"Map size: {nb_rows}x{nb_cols}" )
    return tiles, start

@cache
def get_trail_ends( coords, verbose = False ) :
    # get coordinates tuple as params because it needs to be hashable to use cache...
    tile = TILES[ coords ]
    if verbose :
        print( f"Trail ends for tile @{tile[ 'coords' ]}, height {tile[ 'height' ]} ..." )
    ends = set()
    if tile[ "height" ] == END :
        ends.add( coords )
    else :
        ends = set()
        for next_coords in tile[ "next" ] :
            ends = ends.union( get_trail_ends( next_coords, verbose ) )
    if verbose or ( tile[ "height" ] == START ) :
        print( f"Trail ends for tile @{tile[ 'coords' ]}, height {tile[ 'height' ]} : {len(ends)} ends found" )
    return ends

def do_problem( str_data, verbose = False ) :
    global TILES
    TILES, start = parse_data( str_data, verbose )
    nb_trails = 0
    for coords in start :
        nb_trails += len( get_trail_ends( coords, verbose ) )
    print( f"{nb_trails} trails found from {len(start)} starting points" )

def do_tests() :
    str_data = get_file_content( get_test_file_path(), True )
    do_problem( str_data, True )

def do_input() :
    str_data = get_file_content( get_input_file_path(), True )
    do_problem( str_data, False )

def main() :
    start = time.time()
    #do_check(  )
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
