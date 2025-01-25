#!/usr/bin/env python3

import os
import time
from collections import namedtuple
import re
from typing import Callable
from termcolor import colored

def get_test_file_path( i = None ) :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

Coordinate = namedtuple( "Coordinate", [ "x", "y" ] )
Node = namedtuple( "Node", [ "estimated_cost", "heuristic_to_end", "cost_from_start",
                            "from_state", "state" ] )
Maze = namedtuple( "Maze", [ "width", "height", "tiles", "start", "end" ] )

COORDINATE_RE = re.compile( r"^(?P<x>\d+),(?P<y>\d+)$" )
TILE_FREE = "."
TILE_PATH = "O"
TILE_NONE = "#"

def parse_data( str_data: str, maze_max: int, verbose: bool = False ) :
    coordinates = []
    for line in str_data.split( "\n" ) :
        match = COORDINATE_RE.match( line )
        if match is not None :
            match = match.groupdict()
            coords = Coordinate( int( match[ "x" ] ), int( match[ "y" ] ) )
            coordinates.append( coords )
    tiles = dict()
    width, height = maze_max + 1, maze_max + 1
    for x in range( width ) :
        for y in range( height ) :
            tiles[ Coordinate( x, y ) ] = TILE_FREE
    start = Coordinate( 0, 0 )
    end = Coordinate( maze_max, maze_max )
    maze = Maze( width, height, tiles, start, end )
    return coordinates, maze

def print_maze( maze: Maze, path = None, cost = None, highlights = None, verbose = False ) :
    if highlights is None :
        highlights = []
    print()
    print( f"Maze {maze.width}x{maze.height}:" )
    if path is None :
        tiles = maze.tiles
    else :
        # path is a list of positions
        # for each element of the path (except start & end of the maze)
        # we replace the empty PATH_TILE "." with the direction
        tiles = maze.tiles.copy() # we don't want to alter the original maze
        for coord in path :
            tiles[ coord ] = TILE_PATH
    for y in range( maze.height ) :
        line = ""
        for x in range( maze.width ) :
            coord = Coordinate( x, y )
            if coord in highlights :
                line += colored( tiles.get( coord, TILE_NONE ), 'red' )
            else :
                line += tiles.get( coord, TILE_NONE )
        print( line )
    print( f"Start: @{maze.start}, End: @{maze.end}" )
    if path is not None :
        print( f"Path length: {len(path)} tile(s)" )
    if cost is not None :
        print( f"Cost of path: {cost}" )
    print()

def get_neighbours( state: Coordinate , maze: Maze, verbose = False ) :
    candidates = [
        Coordinate( state.x + 1, state.y     ),
        Coordinate( state.x    , state.y + 1 ),
        Coordinate( state.x - 1, state.y     ),
        Coordinate( state.x    , state.y - 1 ),
    ]
    neighbours = [ neighbour for neighbour in candidates if neighbour in maze.tiles ]
    return neighbours

def heuristic_distance( state: Coordinate, maze: Maze, verbose: bool = False ) -> int :
    # we define the heuristic as the "minimum" cost to reach the maze end,
    # as if there were no walls beetween the state and the end of the maze
    # and without taking turns into account
    delta_x, delta_y = maze.end.x - state.x, maze.end.y - state.y
    distance = abs( delta_x ) + abs( delta_y )
    return distance

def get_move_cost( a: Coordinate, b: Coordinate, verbose: bool = False ) -> int :
    # we assume a and b are neighbour positions
    return 1

def make_node( state, maze, from_node = None,
              heuristic: Callable[ [Coordinate, Maze, bool], int ] = heuristic_distance,
              verbose: bool = False ) -> Node :
    heuristic_to_end = heuristic( state, maze, verbose )
    if from_node is not None :
        from_state = from_node.state
        cost_from_start = from_node.cost_from_start + get_move_cost( from_state, state, verbose )
    else :
        # starting node
        from_state = None
        cost_from_start = 0
    estimated_cost = cost_from_start + heuristic_to_end
    return Node( estimated_cost, heuristic_to_end, cost_from_start, from_state, state )

def add_open_node( open_set: dict[ Coordinate, Node ], state: Coordinate, maze: Maze,
                  heuristic: Callable[ [Coordinate, Maze, bool], int ] = heuristic_distance,
                  from_node: Node = None, verbose: bool = False ) -> dict[ Coordinate, Node ] :
    node = make_node( state, maze, from_node, heuristic, verbose )
    if state in open_set :
        old_node = open_set[ state ]
        if node.estimated_cost < old_node.estimated_cost :
            open_set[ state ] = node
    else :
        open_set[ state ] = node
    return open_set

def get_next_open_node( open_set: dict[ Coordinate, Node ] ) -> tuple[ dict[ Coordinate, Node ], Node ] :
    next_open_node = min( open_set.values() )
    open_set.pop( next_open_node.state )
    return open_set, next_open_node

def a_star( maze: Maze,
           heuristic: Callable[ [Coordinate, Maze, bool], int ] = heuristic_distance,
           starting_state: Coordinate = None,
           verbose: bool = False ) -> tuple[ list[ Coordinate ], int ] :
    # initialisation
    if starting_state is None :
        starting_state = maze.start
    open_set = dict()
    open_set = add_open_node( open_set, starting_state, maze, heuristic, None, verbose )
    closed_set = dict()
    # loop: main algorithm
    print( f"Searching for a path from @{starting_state} to @{maze.end}" )
    while len( open_set ) > 0 :
        open_set, current_node = get_next_open_node( open_set )
        closed_set[ current_node.state ] = current_node
        for neighbour_state in get_neighbours( current_node.state, maze, verbose ) :
            if neighbour_state == maze.end :
                # we reached the end and found _A_ shortest path
                print( f"End reached @{neighbour_state}" )
                end_node = make_node( neighbour_state, maze, current_node, heuristic, verbose )
                print( f"Cost to reach the end: {end_node.cost_from_start}" )
                path = trace_path( end_node, closed_set, verbose )
                return path, end_node.cost_from_start
            if neighbour_state not in closed_set :
                # if the node was not already processed, we add it to the open set
                open_set = add_open_node(
                    open_set, neighbour_state, maze, heuristic, current_node, verbose
                )
    print( f"UNABLE TO FIND A PATH!!!" )
    return None, None

def trace_path( end_node: Node, closed_set: dict[ Coordinate, Node ],
               verbose: bool = False ) -> list[ Coordinate ] :
    path = [ end_node.state ]
    predecessor_node = closed_set.get( end_node.from_state, None )
    while predecessor_node is not None :
        path.append( predecessor_node.state )
        predecessor_node = closed_set.get( predecessor_node.from_state, None )
    path.reverse() # reverse to get the path from start to end
    return path

def fall( coordinates, maze, nb_turns, verbose = False ) :
    print( f"Making {nb_turns} stones fall..." )
    fallen = coordinates[0:nb_turns]
    remaining = coordinates[nb_turns:]
    wrecked_maze = Maze( maze.width, maze.height, maze.tiles.copy(), maze.start, maze.end )
    for coord in fallen :
        if verbose :
            print( f"Stone falling @{coord}" )
        wrecked_maze.tiles.pop( coord )
    return remaining, wrecked_maze

def find_first_blocked( coordinates, maze, verbose = False ) :
    # the path is free when one stone has fallen (we use 1 to avoid index errors)
    # we assume the path is blocked when all the stones have fallen
    last_free, first_blocked = 1, len( coordinates )
    while first_blocked - last_free > 1 :
        test_fall = last_free + ( first_blocked - last_free ) // 2
        print( f"Testing stone #{test_fall}, falling @{coordinates[test_fall]}" )
        remaining, wrecked_maze = fall( coordinates, maze, test_fall, verbose=False )
        path, cost = a_star( wrecked_maze, heuristic_distance, None, verbose=False )
        if path is None :
            first_blocked = test_fall
        else :
            last_free = test_fall
    print( f"Last stone leaving the path free is #{last_free} @{coordinates[last_free - 1]}" )
    print( f"First stone blocking the path is #{first_blocked} @{coordinates[first_blocked - 1]}" )
    return first_blocked, coordinates[first_blocked - 1]

def do_problem( str_data: str, maze_max: int, verbose = False ) :
    coordinates, maze = parse_data( str_data, maze_max, verbose )
    print_maze( maze )
    first_blocked, blocked_coord = find_first_blocked( coordinates, maze, verbose )
    remaining, blocked_maze = fall( coordinates, maze, first_blocked, verbose )
    print_maze( blocked_maze, highlights = [ blocked_coord ] )
    print( f"First stone blocking the path is #{first_blocked} @{blocked_coord}" )
    print( f"Answer: {blocked_coord.x},{blocked_coord.y}" )
    print( f"END" )

def do_tests( i = None ) :
    str_data = get_file_content( get_test_file_path( i ) )
    do_problem( str_data, 6, True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, 70, False )

def main() :
    os.system('color')
    start = time.time()
    #do_tests(1)
    #do_tests(2)
    #do_tests(3)
    #do_tests(4)
    #do_tests(5)
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
