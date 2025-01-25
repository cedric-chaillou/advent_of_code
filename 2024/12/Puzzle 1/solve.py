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

TILES = {}

def add_neighbour( tile, neighbour ) :
    if neighbour[ "plant" ] == tile[ "plant" ] :
        # we connect the tiles with the same plant
        tile[ "next_to" ].add( neighbour[ "coords" ] )
        neighbour[ "next_to" ].add( tile[ "coords" ] )

def parse_data( str_data, verbose = False ) :
    tiles = {}
    nb_rows = len( str_data )
    nb_cols = 0
    for row, line in enumerate( [ l.strip() for l in str_data ] ) :
        if row == 0 :
            nb_cols = len( line )
        if verbose :
            print( f"Row {row}: {line}" )
        for col, plant in enumerate( list( line ) ) :
            coords = ( row, col )
            #print( f"Coords: {coords}, height: {height}" )
            tile = {
                "coords" : coords,
                "plant" : plant,
                "next_to" : set(),
            }
            if row > 0 :
                add_neighbour( tile, tiles[ ( row - 1, col ) ] )
            if col > 0 :
                add_neighbour( tile, tiles[ ( row, col - 1 ) ] )
            tiles[ coords ] = tile
    print( f"Map size: {nb_rows}x{nb_cols}" )
    return tiles

def find_region( coords, regions ) :
    for region in regions :
        if coords in region :
            return region
    return None

def add_to_region( coords, region, verbose = False ) :
    if coords not in region :
        region.add( coords )
        tile = TILES[ coords ]
        if verbose :
            print( f"Tile @{coords} ADDED to region for plant {tile['plant']}" )
        for neighbour_coords in tile[ "next_to" ] :
            add_to_region( neighbour_coords, region, verbose )

def get_regions( verbose = False ) :
    regions = []
    for coords in TILES :
        # Is the tile is already mapped in a region ?...
        region = find_region( coords, regions )
        if region is None :
            tile = TILES[ coords ]
            if verbose :
                print( f"NEW region for plant {tile['plant']}, starting @{coords}" )
            # if not => we create a new region !
            region = set()
            add_to_region( coords, region, verbose )
            print( f"NEW region for plant {tile['plant']} created with {len(region)} tiles, starting @{coords}" )
            if verbose :
                print( f"Region: {region}" )
            regions.append( region )
    return regions

def get_region_plant( region ) :
    for coords in region :
        plant = TILES[ coords ][ "plant" ]
        break
    return plant

def get_region_perimeter( region, plant, verbose = False ) :
    perimeter = 0
    for coords in region :
        perimeter += 4 - len( TILES[ coords ][ "next_to" ] )
    return perimeter

def get_region_cost( region, verbose = False ) :
    plant = get_region_plant( region )
    area = len(region)
    perimeter = get_region_perimeter( region, plant, verbose )
    cost = area * perimeter
    print( f"Region for plant {plant}: fence will cost {cost} (area {area}, perimeter {perimeter})" )
    return cost

def do_problem( str_data, verbose = False ) :
    global TILES
    TILES = parse_data( str_data, verbose )
    fence_cost = 0
    regions = get_regions( verbose )
    for region in regions :
        fence_cost += get_region_cost( region, verbose )
    print( f"Total fence cost: {fence_cost} for {len(regions)} regions" )

def do_tests() :
    str_data = get_file_content( get_test_file_path(), True )
    do_problem( str_data, True )

def do_input() :
    str_data = get_file_content( get_input_file_path(), True )
    do_problem( str_data, False )

def main() :
    start = time.time()
    #do_check(  )
    do_tests()
    #do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
