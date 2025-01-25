#!/usr/bin/env python3

import time
from collections import namedtuple
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

robot_re = re.compile( r"^p=(?P<px>[-+]?\d+),(?P<py>[-+]?\d+) v=(?P<vx>[-+]?\d+),(?P<vy>[-+]?\d+)$" )

Position = namedtuple( "Position", [ "x", "y" ] )
Vector = namedtuple( "Vector", [ "x", "y" ] )
Grid = namedtuple( "Grid", [ "width", "height", "robots" ] )
Zone = namedtuple( "Zone", [ "start_x", "start_y", "width", "height" ] )

def parse_data( str_data, verbose = False ) :
    robots = []
    for id, line in enumerate( str_data ) :
        if verbose :
            print( f"Line #{id}" )
        match = robot_re.match( line.strip() ).groupdict()
        position = Position( x=int(match["px"]), y=int(match["py"]) )
        vector = Vector( x=int(match["vx"]), y=int(match["vy"]) )
        robot = ( id, position, vector )
        print( f"New robot: {robot}" )
        robots.append( robot )
    print( f"Nb of robots: {len(robots)}" )
    return robots

def count_robots( x, y, robots ) :
    count = 0
    for id, position, vector in robots :
        if position == ( x, y ) :
            count += 1
    return count

EMPTY = "."
def print_grid( grid, verbose = False ) :
    print()
    print( f"Grid {grid.width}x{grid.height}:" )
    for y in range( grid.height ) :
        line = ""
        for x in range( grid.width ) :
            nb_robots = count_robots( x, y, grid.robots )
            line += str(nb_robots) if nb_robots > 0 else EMPTY
        print( line )
    print()

def move_robots( grid, nb_iterations, verbose = False ) :
    for index, robot in enumerate( grid.robots ) :
        id, position, vector = robot
        # since the vectors are constant, we can do all the iterations at once !
        new_x = ( position.x + nb_iterations * vector.x ) % grid.width
        new_y = ( position.y + nb_iterations * vector.y ) % grid.height
        new_position = Position( x=new_x, y=new_y )
        grid.robots[ index ] = ( id, new_position, vector )
        if verbose :
            print (f"Robot #{id} moved from {position} to {new_position} in {nb_iterations}s" )
    return grid

def get_safety_factor( grid, verbose = False ) :
    quadrant_width = ( grid.width - 1 ) // 2
    quadrant_height = ( grid.height - 1 ) // 2
    if verbose :
        print( f"4 Quadrants {quadrant_width}x{quadrant_height}" )
    quadrants = [
        Zone( start_x=0, start_y=0, width=quadrant_width, height=quadrant_height ),
        Zone( start_x=quadrant_width + 1, start_y=0, width=quadrant_width, height=quadrant_height ),
        Zone( start_x=0, start_y=quadrant_height + 1, width=quadrant_width, height=quadrant_height ),
        Zone( start_x=quadrant_width + 1, start_y=quadrant_height + 1, width=quadrant_width, height=quadrant_height ),
    ]
    if verbose :
        print( f"Quadrants:" )
        for quadrant in quadrants :
            print( f"    {quadrant}" )
    safety_factor = 1
    for i, quadrant in enumerate( quadrants ) :
        nb_robots = 0
        for y in range( quadrant.height ) :
            for x in range( quadrant.width ) :
                nb_robots += count_robots( quadrant.start_x + x, quadrant.start_y + y, grid.robots )
        print( f"{nb_robots} robots found in quadrant #{i}" )
        safety_factor *= nb_robots
        if safety_factor == 0 :
            print( f"0 robots in last quadrant. Stopping compting safety factor..." )
    print( f"Safety factor: {safety_factor}" )
    return safety_factor

def do_problem( str_data, width, height, nb_iterations, verbose = False ) :
    robots = parse_data( str_data, verbose )
    grid = Grid( width=width, height=height, robots=robots )
    if verbose :
        print_grid( grid, verbose = False )
    else :
        print( f"Grid size: {grid.width}x{grid.height}" )
    grid = move_robots( grid, nb_iterations, verbose )
    if verbose :
        print_grid( grid, verbose = False )
    safety_factor = get_safety_factor( grid, verbose )
    print( f"END" )

def do_tests() :
    str_data = get_file_content( get_test_file_path(), True )
    do_problem( str_data, 11, 7, 100, True )

def do_input() :
    str_data = get_file_content( get_input_file_path(), True )
    do_problem( str_data, 101, 103, 100, False )

def main() :
    start = time.time()
    #do_check(  )
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
