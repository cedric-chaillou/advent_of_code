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
ORIGINAL_NOT_VISITED = '.'
NOT_VISITED = ' '
VISITED_UP_DOWN = '|'
VISITED_LEFT_RIGHT = '-'
VISITED_CROSS = '+'
WALL = '#'
OBSTACLE = 'O'
VISITED = {}

def print_infos( room_map, obstacle_position, title = "Map and position" ) :
    print( f"*** {title} ***" )
    print( "Map:" )
    for i, l in enumerate( room_map ) :
        print( f"{''.join(l)}" )
    print( "Obstacle position:", obstacle_position )
    print()

def parse_data( str_data ) :
    #print( "Parsing input data..." )
    room_map = [ list( s ) for s in str_data ]
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
        return tile == WALL or tile == OBSTACLE
    else :
        return False # no wall outside the room (guard exits)

def is_loop_position( visited, guard_pos, in_room ) :
    if not in_room :
        return False, visited
    elif guard_pos in visited :
        return True, visited
    else :
        visited.add( guard_pos )
        return False, visited

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
    # we turn the tile we just 'left' as visited (for map printing purposed only!)
    if dir == 0 or dir == 2 : # up or down
        if room_map[ old_row ][ old_col ] == NOT_VISITED :
            room_map[ old_row ][ old_col ] = VISITED_UP_DOWN
        elif room_map[ old_row ][ old_col ] == VISITED_LEFT_RIGHT :
            room_map[ old_row ][ old_col ] = VISITED_CROSS
        # other cases are not relevant here
    elif dir == 1 or dir == 3 : # left or right
        if room_map[ old_row ][ old_col ] == NOT_VISITED :
            room_map[ old_row ][ old_col ] = VISITED_LEFT_RIGHT
        elif room_map[ old_row ][ old_col ] == VISITED_UP_DOWN :
            room_map[ old_row ][ old_col ] = VISITED_CROSS
        # other cases are not relevant here
    if is_wall( room_map, row, col ) :
        # guard can't advance !
        # stay in place position & turn right
        row, col, dir = old_row, old_col, ( dir + 1 ) % 4
    return ( row, col, dir ), is_in_room( room_map, row, col )

def get_path( room_map, guard_pos, in_room ) :
    loop = False
    visited = set()
    visited.add( guard_pos )
    while in_room and not loop :
        guard_pos, in_room = move_guard( room_map, guard_pos )
        loop, visited = is_loop_position( visited, guard_pos, in_room )
    return loop, visited

def test_obstacle( str_data, coordinates ) :
    room_map, guard_pos, in_room = parse_data( str_data )
    row, col = coordinates
    room_map[ row ][ col ] = OBSTACLE
    loop, visited = get_path( room_map, guard_pos, in_room )
    if loop :
        print_infos( room_map, ( row, col ), title = "SUCCESS! Guard is looping" )
    return loop

def do_problem( str_data ) :
    nicer_data = []
    for line in str_data :
        nicer_data.append( line.strip().replace( ORIGINAL_NOT_VISITED, NOT_VISITED ) )
    room_map, guard_pos, in_room = parse_data( nicer_data )
    print( "Getting default guard path..." )
    loop, visited_path = get_path( room_map, guard_pos, in_room )
    start_row, start_col, start_dir = guard_pos
    test_positions = set()
    for row, col, dir in visited_path :
        if row == start_row and col == start_col :
            # we do not try to put an obstacle on the guard starting position !
            continue
        else :
            test_positions.add( ( row, col ) )
    print( f"{len(test_positions)} obstacle positions to test..." )
    obstacles_list = []
    for test_position in test_positions :
        if test_obstacle( nicer_data, test_position ) :
            obstacles_list.append( test_position )
    print( f"List of obstacle positions: {obstacles_list}" )
    print( f"Nb of obstacles positions found: {len(obstacles_list)}" )

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
