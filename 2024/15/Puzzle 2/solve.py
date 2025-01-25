#!/usr/bin/env python3

import time
from collections import namedtuple
import re

def get_simple_test_file_path() :
    return "tests_simple.txt"

def get_test_file_path() :
    return "tests.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

robot_re = re.compile( r"^p=(?P<px>[-+]?\d+),(?P<py>[-+]?\d+) v=(?P<vx>[-+]?\d+),(?P<vy>[-+]?\d+)$" )

Coordinate = namedtuple( "Coordinate", [ "x", "y" ] )
Vector = namedtuple( "Vector", [ "name", "dx", "dy" ] )
Grid = namedtuple( "Grid", [ "width", "height", "tiles" ] )
Box = namedtuple( "Box", [ "x", "y", "width", "height" ] )

BOX = "O"
WALL = "#"
ROBOT = "@"
EMPTY = "."

BOX_REPR = [ "[]" ]

MOVE_VECTORS = {
    "^" : Vector( name="up"   , dx= 0, dy=-1 ),
    "v" : Vector( name="down" , dx= 0, dy=+1 ),
    "<" : Vector( name="left" , dx=-1, dy= 0 ),
    ">" : Vector( name="right", dx=+1, dy= 0 ),
}

def parse_data( str_data, verbose = False ) :
    tiles = dict()
    robot=None
    moves=""
    is_grid_part = True
    width, height = None, None
    for row, line in enumerate( str_data.split("\n") ) :
        if verbose :
            print( f"Line #{row}" )
        if line == "" :
            # empty line marks the end of the grid and start of the moves
            if height == None :
                height = row
            is_grid_part = False
            continue
        if is_grid_part :
            if width == None :
                width = 2 * len( line )
            for col, tile in enumerate( line ) :
                pos_left = Coordinate( x=2*col, y=row )
                pos_right = Coordinate( x=2*col+1, y=row )
                if tile in [ WALL, ] :
                    tiles[ pos_left ] = tile
                    tiles[ pos_right ] = tile
                    if verbose :
                        print( f"Tiles {tile}{tile} added @{pos_left}-@{pos_right}" )
                elif tile == BOX :
                    tiles[ pos_left ] = BOX_REPR[0][0]
                    tiles[ pos_right ] = BOX_REPR[0][1]
                    if verbose :
                        print( f"Tiles {''.join(BOX_REPR)} added @{pos_left}-@{pos_right}" )
                elif tile == ROBOT :
                    robot = pos_left
                    if verbose :
                        print( f"Robot found @{pos_left}" )
        else :
            moves += line
    grid = Grid( width, height, tiles )
    return grid, robot, moves

def print_grid( grid, robot, verbose = False ) :
    print()
    print( f"Grid {grid.width}x{grid.height}:" )
    for y in range( grid.height ) :
        line = ""
        for x in range( grid.width ) :
            position = Coordinate( x, y )
            if position == robot :
                line += ROBOT
            else :
                line += grid.tiles.get( position, EMPTY )
        print( line )
    print( f"Robot position: @{robot}" )
    print()

def gps( position ) :
    return 100 * position.y + position.x

def sum_boxes_gps( grid ) :
    sum_gps = 0
    for key, value in grid.tiles.items() :
        if value == BOX_REPR[0][0] :
            sum_gps += gps( key )
    return sum_gps

def get_needed_tiles( grid: Grid, box: Box, vector: Vector, verbose = False ) :
    # new tiles are not "needed" if they'll still be used by the same box after the move
    if box is None :
        raise ValueError( f"[get_needed_tiles] box parameter cannot be None" )
    tiles = []
    for x in range( box.x, box.x + box.width ) :
        for y in range( box.y, box.y + box.height ) :
            new_tile = Coordinate( x + vector.dx, y + vector.dy )
            occupied = get_box( grid, new_tile )
            if occupied is None or occupied != box :
                # there is no box on the new tile (free or wall), or there is ANOTHER box
                tiles.append( new_tile )
    return tiles

def check_move( grid: Grid, box: Box, vector: Vector, verbose = False ) :
    #print( f"[check_move] box @{box}, vector @{vector}" )
    needed_tiles = get_needed_tiles( grid, box, vector, verbose )
    #print( f"[check_move] needed free tiles to move: {needed_tiles}" )
    # we need these tiles to be free in order to move the box
    if any( is_wall( grid, tile ) for tile in needed_tiles ) :
        # there is a wall in the way, or we are out of bounds : we cannot move the box
        if verbose :
            print( f"Cannot move {vector.name} box @{box} into the wall" )
        return False, None
    if all( is_free( grid, tile ) for tile in needed_tiles ) :
        # all destination tiles are free : we can move the box
        if verbose :
            print( f"Can move {vector.name} box @{box} into free space" )
        return True, []
    # there must be a box (or more) in the way...
    # set of boxes that are in the way : the "next boxes" which will have to be moved
    # before we can move the current box
    next_box_set = set( get_box( grid, tile ) for tile in needed_tiles )
    if None in next_box_set :
        next_box_set.remove( None )
    # box_tower is a list of set of boxes which must be moved to move the current box
    # the last set is the list is the furthest from the box and will need to be moved first
    # init: the set of "next boxes" we just calculated
    box_tower = [ next_box_set ]
    can_move = True
    for next_box in next_box_set :
        can_move_box, next_box_tower = check_move( grid, next_box, vector, verbose )
        can_move = can_move and can_move_box
        if can_move :
            # we need to add the "next box sets" to the current one
            # level 0 of the box tower is "next_box_set"
            # level 1+ are the union of the bos sets of each "next box"
            for i, bs in enumerate( next_box_tower, 1 ) :
                if len( box_tower ) == i :
                    # there is no box set at this depth : we add the set "as is"
                    box_tower.append( bs )
                else :
                    # there is already a set at this depth : we add to it
                    box_tower[ i ] = box_tower[ i ].union( bs )
        else :
            if verbose :
                print( f"Cannot move {vector.name} box @{box} into another box" )
            return False, None
    # return result of iteration and recursive calls
    if verbose :
        print( f"Can move {vector.name} box @{box} after moving {', then '.join( [ str(len(bs)) for bs in reversed(box_tower) ] )} box(es)" )
    return can_move, box_tower

def get_box( grid: Grid, tile: Coordinate, verbose = False ) :
    """
    Returns the box if the tile is occupied by a box

    Args:
        grid (Grid): the whole grid
        tile (Coordinate): the tile coordinates to check
        verbose (bool, optional): defaults to False.

    Returns:
        - if the tile contains a box: a tuple with all the coordinates occupied by the box
        - otherwise: None
    """
    content = grid.tiles.get( tile, None )
    if content is not None and content in "".join(BOX_REPR) :
        # where are we in the box ?
        # we assume the character representing the top left corner of the box is unique
        # and same for the characters representing top border of the box (first line)
        # and we search for the top left coordinates of the box
        top_left_char = BOX_REPR[0][0]
        dx, dy = 0, 0
        top_left_tile = tile
        while content != top_left_char :
            if content in BOX_REPR[0] :
                dx -= BOX_REPR[0].index( content )
            else :
                dy -= 1
            top_left_tile = Coordinate( tile.x + dx, tile.y + dy )
            content = grid.tiles.get( top_left_tile, None )
        return Box( x=top_left_tile.x, y=top_left_tile.y, width=len(BOX_REPR[0]), height=len(BOX_REPR) )
    else :
        return None

def do_move_box( grid: Grid, box: Box, vector: Vector, verbose = False ) :
    # we don't check that we can move the box: this should have already been done...
    new_box = Box( box.x + vector.dx, box.y + vector.dy, box.width, box.height )
    if verbose :
        print( f"Moving {vector.name} box from @{box} to @{new_box}" )
    # first we delete the box at the old coordinates
    for x in range( box.x, box.x + box.width ) :
        for y in range( box.y, box.y + box.height ) :
            tile = Coordinate( x, y )
            grid.tiles.pop( tile, None )
    # then we add the box at the new coordinates
    for dx in range( new_box.width ) :
        for dy in range( new_box.height ) :
            tile = Coordinate( new_box.x + dx, new_box.y + dy )
            grid.tiles[ tile ] = BOX_REPR[dy][dx]


    return grid

def make_free( grid, tile, vector, verbose = False ) :
    # if the tile contains a box, we move the box (if we can)
    # we push other boxes along the way if necessary
    box = get_box( grid, tile, verbose )
    if box is not None :
        can_push, box_tower = check_move( grid, box, vector, verbose )
        if can_push :
            box_tower = [ { box } ] + box_tower
            if verbose :
                print( f"Moving {vector.name} box(es) to free tile @{tile}..." )
            # Do the push for the whole box tower...
            for box_set in reversed( box_tower ) :
                if verbose :
                    print( f"- {', '.join( [ str(b) for b in box_set ] )}" )
                for b in box_set :
                    grid = do_move_box( grid, b, vector, verbose )
        else :
            if verbose :
                print( f"Cannot push box(es) to free tile @{tile}" )
    else :
        if verbose :
            print( f"No box found @{tile}" )
    return grid

def is_free( grid, tile ) :
    return grid.tiles.get( tile, None ) is None

def is_wall( grid, tile ) :
    # nota: all out of bounds tiles are "walls"
    return grid.tiles.get( tile, None ) == WALL or not_in_grid( grid, tile )

def not_in_grid( grid, tile ) :
    return tile.x < 0 and tile.y < 0 and tile.x >= grid.width and tile.y >= grid.height

def move_robot( grid, robot, move, verbose = False ) :
    vector = MOVE_VECTORS.get( move, None )
    if vector is not None :
        new_robot = Coordinate( robot.x + vector.dx, robot.y + vector.dy )
        # first we free the destination tile, if necessary:
        grid = make_free( grid, new_robot, vector, verbose )
        if is_free( grid, new_robot ) :
            # destination tile is empty => robot can move
            print( f"Robot moves {vector.name} from @{robot} to @{new_robot}" )
            if verbose :
                print_grid( grid, new_robot, verbose )
            return grid, new_robot
        else :
            # destination tile is occupied => robot cannot move
            if verbose :
                print( f"Robot cannot move {vector.name} from @{robot} into {grid.tiles[ new_robot ]}" )
            return grid, robot

def do_problem( str_data, verbose = False ) :
    grid, robot, moves = parse_data( str_data, verbose )
    print_grid( grid, robot, verbose )
    print( f"{len(moves)} moves programmed" )
    if verbose :
        print( f"Moves: {moves}" )
    print()
    print( f"Executing moves..." )
    for move in moves :
        grid, robot = move_robot( grid, robot, move, verbose )
    print_grid( grid, robot, verbose )
    print()
    sum_gps = sum_boxes_gps( grid )
    print( f"Sum of Goods Positioning System: {sum_gps}")
    print( f"END" )

def do_simple_tests() :
    str_data = get_file_content( get_simple_test_file_path() )
    do_problem( str_data, True )

def do_tests() :
    str_data = get_file_content( get_test_file_path() )
    do_problem( str_data, True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, False )

def main() :
    start = time.time()
    #do_simple_tests()
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
