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

def get_tile_sides( row, col ) :
    tile = TILES[ ( row, col ) ]
    sides = []
    # test for sides oriented towards the north (N), east (E), south (S) & west (W) :
    # side def : orientation (towards the outside), start row & col, end row & col
    # if we stand in the tile (the region) facing the side, it starts on the left and ends on the right
    # coordinates for start of the side are always the neighbour coordinates for the orientation
    # we don't need to check for map boundaries because the border of the map is always a side
    possible_sides = [
        ( 'N', row - 1, col, row - 1, col + 1 ), # same row, north of the tile, going towards the east
        ( 'E', row, col + 1, row + 1, col + 1 ), # same col, east of the tile, going towards the south
        ( 'S', row + 1, col, row + 1, col - 1 ), # same row, south of the tile, going towards the west
        ( 'W', row, col - 1, row - 1, col - 1 ), # same col, west of the tile, going towards the north
    ]
    for orientation, start_row, start_col, end_row, end_col in possible_sides :
        if ( start_row, start_col ) not in tile[ "next_to" ] :
            sides.append( ( orientation, ( start_row, start_col ), ( end_row, end_col ) ) )
    return sides

def side_sort_key( side ) :
    orientation, start, end = side
    start_row, start_col = start
    key = ( orientation, )
    if orientation == 'N' :
        # sort for "horizontal" fence oriented towards the north (N)
        # we sort by row, then going to the right (E) (by column ascending)
        key += ( start_row, start_col )
    elif orientation == 'E' :
        # sort for "vertical" fence oriented towards the east (E)
        # we sort by column, then going down (S) (by row ascending)
        key += ( start_col, start_row )
    elif orientation == 'S' :
        # sort for "horizontal" fence oriented towards the south (S)
        # we sort by row, then going to the left (W) (by column descending)
        key += ( start_row, -start_col )
    elif orientation == 'W' :
        # sort for "vertical" fence oriented towards the west (W)
        # we sort by column, going up (N) (by row descending)
        key += ( start_col, -start_row )
    return key

def merge_region_sides( sides, plant, verbose = False ) :
    print( f"Merging sides for region of plant {plant} ..." )
    sides.sort( key = side_sort_key )
    last_orientation, last_start, last_end = None, None, None
    new_sides = []
    for side_orientation, side_start, side_end in sides :
        if side_orientation == last_orientation and side_start == last_end :
            # side is contiguous to previous side : we merge
            new_sides[ len( new_sides ) - 1 ] = ( last_orientation, last_start, side_end )
            if verbose :
                print( f"Merged side: {new_sides[ len( new_sides ) - 1 ]}" )
        else :
            # side is non contiguous (either a gap, not the same row or col, or a different orientation)
            new_sides.append( ( side_orientation, side_start, side_end ) )
            if verbose :
                print( f"New side: {new_sides[ len( new_sides ) - 1 ]}" )
        last_orientation, last_start, last_end = new_sides[ len( new_sides ) - 1 ]
    if verbose :
        print( f"Sides of region for plant {plant}: {new_sides}" )
    return new_sides

def get_region_sides( region, plant, verbose = False ) :
    sides = []
    for row, col in region :
        sides += get_tile_sides( row, col )
    sides = merge_region_sides( sides, plant, verbose )
    print( f"{len(sides)} sides calculated for region" )
    return sides

def get_region_cost( region, verbose = False ) :
    plant = get_region_plant( region )
    area = len(region)
    nb_sides = len( get_region_sides( region, plant, verbose ) )
    cost = area * nb_sides
    print( f"Region for plant {plant}: fence will cost {cost} (area {area}, {nb_sides} sides)" )
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
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
