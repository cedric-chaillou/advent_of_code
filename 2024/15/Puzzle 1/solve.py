#!/usr/bin/env python3

import time
from collections import namedtuple
import re

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
BOX = "O"
WALL = "#"
ROBOT = "@"
EMPTY = "."

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
                width = len( line )
            for col, tile in enumerate( line ) :
                position = Coordinate( x=col, y=row )
                if tile in [ BOX, WALL ] :
                    tiles[ Coordinate( x=col, y=row ) ] = tile
                    if verbose :
                        print( f"Tile {tile} added @{position}" )
                elif tile == ROBOT :
                    robot = Coordinate( x=col, y=row )
                    if verbose :
                        print( f"Robot found @{position}" )
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
        if value == BOX :
            sum_gps += gps( key )
    return sum_gps

def push_box( grid, tile, vector, verbose ) :
    # if the tile contains a box, we move it
    if grid.tiles.get( tile, None ) == BOX :
        next_tile = Coordinate( tile.x + vector.dx, tile.y + vector.dy )
        # first we free the next tile, if necessary:
        grid = push_box( grid, next_tile, vector, verbose )
        if grid.tiles.get( next_tile, None ) is None :
            # next tile is free => the box can be pushed
            if verbose :
                print( f"Pushing box {vector.name} from @{tile} to @{next_tile}" )
            grid.tiles[ next_tile ] = grid.tiles[ tile ] # copy the tile to next_tile
            grid.tiles.pop( tile, None ) # free the tile (remove tile from tiles dict)
        else :
            # next tile is occupied => the box cannot be pushed
            if verbose :
                print( f"Cannot push box {vector.name} from @{tile} into {grid.tiles[ next_tile ]}" )
    return grid

def move_robot( grid, robot, move, verbose = False ) :
    vector = MOVE_VECTORS.get( move, None )
    if vector is not None :
        new_robot = Coordinate( robot.x + vector.dx, robot.y + vector.dy )
        # first we free the destination tile, if necessary:
        grid = push_box( grid, new_robot, vector, verbose )
        if grid.tiles.get( new_robot, None ) is None :
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

def do_tests() :
    str_data = get_file_content( get_test_file_path() )
    do_problem( str_data, True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, False )

def main() :
    start = time.time()
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
