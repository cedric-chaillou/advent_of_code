#!/usr/bin/env python3

import time
from collections import namedtuple
import re

def get_test_file_path( i = None ) :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

robot_re = re.compile( r"^p=(?P<px>[-+]?\d+),(?P<py>[-+]?\d+) v=(?P<vx>[-+]?\d+),(?P<vy>[-+]?\d+)$" )

Coordinate = namedtuple( "Coordinate", [ "x", "y" ] )
Vector = namedtuple( "Vector", [ "dx", "dy" ] )
State = namedtuple( "State", [ "coord", "dir" ] )
Node = namedtuple( "Node", [ "estimated_cost", "heuristic_to_end", "cost_from_start", "from_state", "state" ] )
Maze = namedtuple( "Maze", [ "width", "height", "tiles", "start", "end" ] )

# the directions expressed as characters (to represent them in the maze)
DIR_REPR = ( ">", "^", "<", "v" )
# the same directions (in the same order) expressed as vectors
DIR_VECTORS = ( Vector(+1,0), Vector(0,-1), Vector(-1,0), Vector(0,+1) )

START_TILE = "S"
END_TILE = "E"
PATH_TILE = "."
WALL_TILE = "#"
START_DIR = ">"

COST_STEP = 1
COST_TURN = 1000

def parse_data( str_data, verbose = False ) :
    start, end = None, None
    lines = str_data.split( "\n" )
    width, height = len( lines[0] ), len( lines )
    tiles = dict()
    for y, line in enumerate( lines ) :
        for x, char in enumerate( line ) :
            if char == WALL_TILE :
                # we don't map walls...
                continue
            coord = Coordinate( x, y )
            tiles[ coord ] = char
            if char == START_TILE :
                start = State( coord=coord, dir=DIR_REPR.index(START_DIR) )
            elif char == END_TILE :
                end = coord
    maze = Maze( width, height, tiles, start, end )
    return maze

def print_maze( maze, path = None, cost = None, verbose = False ) :
    print()
    print( f"Maze {maze.width}x{maze.height}:" )
    if path is None :
        tiles = maze.tiles
    else :
        # path is a list of positions
        # for each element of the path (except start & end of the maze)
        # we replace the empty PATH_TILE "." with the direction
        tiles = maze.tiles.copy() # we don't want to alter the original maze
        for coord, dir in path :
            if coord not in [ maze.start.coord, maze.end ] :
                tiles[ coord ] = DIR_REPR[ dir ]
    for y in range( maze.height ) :
        line = ""
        for x in range( maze.width ) :
            coord = Coordinate( x, y )
            line += tiles.get( coord, WALL_TILE )
        print( line )
    print( f"Starting state: @{maze.start.coord}, direction: {DIR_REPR[maze.start.dir]}" )
    print( f"End: @{maze.end}" )
    if path is not None :
        print( f"Path length: {len(path)} state(s)" )
    if cost is not None :
        print( f"Path cost: {cost}" )
    print()

def get_neighbours( state: State , maze: Maze, verbose = False ) :
    neighbours = [
        State( state.coord, ( state.dir + 1 ) % len( DIR_VECTORS ) ), # +90° turn, i.e. anti-clockwise
        State( state.coord, ( state.dir - 1 ) % len( DIR_VECTORS ) ), # -90° turn, i.e. clockwise
    ]
    vector = DIR_VECTORS[ state.dir ]
    next_coord = Coordinate( state.coord.x + vector.dx, state.coord.y + vector.dy )
    if next_coord in maze.tiles :
        neighbours.append( State( next_coord, state.dir ) )
    return neighbours

def heuristic( state: State, maze: Maze, verbose: bool = False ) -> int :
    # we define the heuristic as the "minimum" cost to reach the maze end,
    # as if there were no walls beetween the state and the end of the maze
    if state.coord == maze.end :
        # we reached the end !
        return 0
    delta_x, delta_y = maze.end.x - state.coord.x, maze.end.y - state.coord.y
    distance = abs( delta_x ) + abs( delta_y )
    # estimating nb of turns
    vector = DIR_VECTORS[ state.dir ]
    scalar_product = vector.dx * delta_x + vector.dy * delta_y
    if ( delta_x != 0 and delta_y != 0 ) :
        # both delta are non zero
        nb_turns = 1 if scalar_product > 0 else 2
    else :
        # one delta (and only one) is zero
        # i.e. coordinates are on the same line or row as the end of the maze
        nb_turns = 0 if scalar_product > 0 else 1 if scalar_product == 0 else 2
    return nb_turns * COST_TURN + distance * COST_STEP

def get_move_cost( a: State, b: State, verbose: bool = False ) -> int :
    # we assume a and b are neighbour positions
    if a.coord == b.coord :
        # if same coordinates, direction is different and we move only by (+/-)90°
        return COST_TURN
    else :
        # if different coordinates, direction is the same and we move only by 1 tile
        return COST_STEP

def make_node( state, maze, from_node = None, verbose: bool = False ) -> Node :
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

def add_open_node( open_set: dict[ State, Node ], state: State, maze: Maze,
                  from_node: Node = None, verbose: bool = False ) -> dict[ State, Node ] :
    node = make_node( state, maze, from_node )
    if state in open_set :
        old_node = open_set[ state ]
        if node.estimated_cost < old_node.estimated_cost :
            open_set[ state ] = node
    else :
        open_set[ state ] = node
    return open_set

def get_next_open_node( open_set: dict[ State, Node ] ) -> tuple[ dict[ State, Node ], Node ] :
    next_open_node = min( open_set.values() )
    open_set.pop( next_open_node.state )
    return open_set, next_open_node

def a_star( maze: Maze, starting_state: State = None,
           verbose: bool = False ) -> tuple[ list[ State ], int ] :
    # initialisation
    if starting_state is None :
        starting_state = maze.start
    open_set = dict()
    open_set = add_open_node( open_set, starting_state, maze, None, verbose )
    closed_set = dict()
    # loop: main algorithm
    print( f"Searching for a path from @{starting_state.coord} to @{maze.end}" )
    while len( open_set ) > 0 :
        open_set, current_node = get_next_open_node( open_set )
        closed_set[ current_node.state ] = current_node
        for neighbour_state in get_neighbours( current_node.state, maze, verbose ) :
            if neighbour_state.coord == maze.end :
                # we reached the end and found _A_ shortest path
                print( f"End reached @{neighbour_state.coord}, direction: {DIR_REPR[neighbour_state.dir]}" )
                end_node = make_node( neighbour_state, maze, current_node, verbose )
                print( f"Cost to reach the end: {end_node.cost_from_start}" )
                path = trace_path( end_node, closed_set, verbose )
                return path, end_node.cost_from_start
            if neighbour_state not in closed_set :
                # if the node was not already processed, we add it to the open set
                open_set = add_open_node( open_set, neighbour_state, maze, current_node, verbose )
    print( f"UNABLE TO FIND A PATH!!!" )
    return None, None

def trace_path( end_node: Node, closed_set: dict[ State, Node ],
               verbose: bool = False ) -> list[ State ] :
    path = [ end_node.state ]
    predecessor_node = closed_set.get( end_node.from_state, None )
    while predecessor_node is not None :
        path.append( predecessor_node.state )
        predecessor_node = closed_set.get( predecessor_node.from_state, None )
    path.reverse() # reverse to get the path from start to end
    return path

def do_problem( str_data, verbose = False ) :
    maze = parse_data( str_data, verbose )
    print_maze( maze, None, None, verbose )
    path, cost = a_star( maze )
    print_maze( maze, path, cost, verbose )
    print( f"END" )

def do_tests( i = None ) :
    str_data = get_file_content( get_test_file_path( i ) )
    do_problem( str_data, True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, False )

def main() :
    start = time.time()
    #do_tests(1)
    #do_tests(2)
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
