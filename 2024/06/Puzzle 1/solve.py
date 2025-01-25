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

DIRECTIONS = ( '^', '>', 'v', '<' )
NOT_VISITED = '.'
VISITED = 'X'
WALL = '#'

def print_infos( room_map, guard_pos, in_room, title = "Map and position" ) :
    print( f"*** {title} ***" )
    print( "Map:" )
    for i, l in enumerate( room_map ) :
        print( f"{i: 4d}    {''.join(l)}" )
    print( "Guard position:", guard_pos )
    print( "Guard is in room?", in_room )
    print()

def parse_data( str_data ) :
    print( "Parsing input data..." )
    room_map = [ list( s.strip() ) for s in str_data ]
    guard_pos = None
    in_room = False
    for row, line in enumerate( room_map ) :
        for dir, char in enumerate( DIRECTIONS ) :
            if char in line :
                col = line.index( char ) # coordonnée colonne
                guard_pos = ( row, col, dir )
                in_room = True
                break
        if in_room :
            break
    return room_map, guard_pos, in_room

def is_in_room( room_map, row, col ) :
    if row < 0 or col < 0 :
        return False
    if row >= len( room_map ) :
        return False
    if col >= len( room_map[ row ] ) :
        return False
    return True

def is_wall( room_map, row, col ) :
    if is_in_room( room_map, row, col ) :
        tile = room_map[ row ][ col ]
        return tile == WALL
    else :
        return False # no wall outside the room (guard exists the room)

def move_guard( room_map, guard_pos ) :
    row, col, dir = guard_pos
    old_row, old_col = row, col
    if dir == 0 : # up ^
        row -= 1
    elif dir == 1 : # right >
        col += 1
    elif dir == 2 : # down v
        row += 1
    else : # dir == 3 ; left <
        col -= 1
    if is_wall( room_map, row, col ) :
        # stay in place position & turn right
        row, col, dir = old_row, old_col, ( dir + 1 ) % 4
    else :
        # we turn the tile we just legft as VISITED
        room_map[ old_row ][ old_col ] = VISITED
    return ( row, col, dir ), is_in_room( room_map, row, col )

def count_tiles( room_map, tile = None ) :
    nb_tile = 0
    for line in room_map :
        if tile is not None :
            nb_tile += line.count( tile )
        else :
            nb_tile += len( line )
    return nb_tile

def do_problem( str_data ) :
    room_map, guard_pos, in_room = parse_data( str_data )
    print_infos( room_map, guard_pos, in_room, title = "Initial map and position" )
    while in_room :
        guard_pos, in_room = move_guard( room_map, guard_pos )
    print_infos( room_map, guard_pos, in_room, title = "Final map and position" )
    nb_tiles_visited = count_tiles( room_map, VISITED )
    print( "Nb of tiles visited by the guard:", nb_tiles_visited )

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
